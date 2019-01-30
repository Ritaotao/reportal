import pandas as pd
from io import StringIO, BytesIO
from .models import Template, Field, Rule, RuleSet
from django.contrib import messages


class Quality:

    def __init__(self, df, rulesets):
        self.err_msg = []
        self.err_detail = []
        self.wrn_msg = []
        self.wrn_detail = []
        self.scs_msg = []
        self.df = df
        self.rulesets = rulesets

    def output(self):
        for ruleset in self.rulesets:
            rule_name = ruleset.rule.name
            if rule_name == 'Greater Equal Than':
                self._gte(ruleset)
            elif rule_name == 'Less Equal Than':
                self._lte(ruleset)
            elif rule_name == 'Unrecognized Value':
                self._unrecog(ruleset)
            elif rule_name == 'Count Underscores':
                self._countus(ruleset)
            elif rule_name == 'Match Regular Expression':
                self._matchre(ruleset)
        return {
            'err_msg': self.err_msg,
            'wrn_msg': self.wrn_msg,
            'scs_msg': self.scs_msg,
            'err_detail': self.err_detail,
            'wrn_detail': self.wrn_detail
        }

    
    def flatten(self, rs_obj):
        # rs_obj: a ruleset object, dict {id, field, rule, action, argument, error_message}
        name, dtype = rs_obj.field.name, rs_obj.field.dtype
        rule_name = rs_obj.rule.name
        action, arg, err_msg = rs_obj.action, rs_obj.argument, rs_obj.error_message
        arg = self.parseArg(rule_name, dtype, arg)
        col = self.df[name].copy()
        return col, name, rule_name, action, arg, err_msg
    
    def parseArg(self, rule_name, dtype, arg):
        if rule_name == 'Unrecognized Value':
            arg_li = [x.strip() for x in arg.split(',')]
            if dtype == 'NUMERIC':
                return [pd.to_numeric(x) for x in arg_li]
            elif dtype == 'DATETIME':
                return [pd.to_datetime(x) for x in arg_li]
            else:
                return arg_li
        elif rule_name == 'Count Underscores':
            return int(arg)
        if dtype == 'NUMERIC':
            return pd.to_numeric(arg)
        elif dtype == 'DATETIME':
            return pd.to_datetime(arg)

    def addMsg(self, name, rule_name, action, arg, err_msg, row_num):
        num_err = len(row_num)
        row_num = ', '.join(str(x) for x in row_num)
        if num_err > 0:
            if action == 'ERROR':
                self.err_msg.append('ERROR: {} values in Column {} failed {} check for {}: {}'.format(num_err, name, rule_name, arg, err_msg))
                self.err_detail.append(row_num)
            else:
                self.wrn_msg.append('WARNING: {} values in Column {} failed {} check for {}: {}'.format(num_err, name, rule_name, arg, err_msg))
                self.wrn_detail.append(row_num)
        else:
            self.scs_msg.append('SUCCESS: Column {} passed {} check for {}'.format(name, rule_name, arg))

    def _gte(self, rs_obj):
        # check value greater and equal than arg
        col, name, rule_name, action, arg, err_msg = self.flatten(rs_obj)  
        row_num = list(col[col < arg].index+2)
        self.addMsg(name, rule_name, action, arg, err_msg, row_num)
    
    def _lte(self, rs_obj):
        # check value less and equal than arg
        col, name, rule_name, action, arg, err_msg = self.flatten(rs_obj)
        row_num = list(col[col > arg].index+2)
        self.addMsg(name, rule_name, action, arg, err_msg, row_num)

    def _unrecog(self, rs_obj):
        # check value within argument list
        col, name, rule_name, action, arg, err_msg = self.flatten(rs_obj)
        row_num = list(col[~col.isin(arg)].index+2)
        self.addMsg(name, rule_name, action, arg, err_msg, row_num)

    def _countus(self, rs_obj):
        # check number of underscores match arg
        col, name, rule_name, action, arg, err_msg = self.flatten(rs_obj)
        row_num = list(col[col.str.count('_') != arg].index+2)
        self.addMsg(name, rule_name, action, arg, err_msg, row_num)

    def _matchre(self, rs_obj):
        # check value match regular expression
        col, name, rule_name, action, arg, err_msg = self.flatten(rs_obj)
        row_num = list(col[~col.str.match(arg)].index+2)
        self.addMsg(name, rule_name, action, arg, err_msg, row_num)


def check_quality(request, input_file, template):
    # input_file: request.FILES['upload']
    file_name = input_file.name
    cxt = {}
    df = pd.DataFrame()

    # read file
    if ".xlsx" in file_name:
        xl = pd.ExcelFile(input_file)
        ## error: only 1 sheet allowed
        if len(xl.sheet_names) > 1:
            messages.error(request, 'ERROR: Please only include one sheet in the excel file')
            return cxt
        else:
            df = pd.read_excel(xl, sheet_name=0, dtype=object)
    else:
        df = pd.read_csv(input_file, dtype=object)
    
    # check column name
    fields = Field.objects.filter(template=template).values('name', 'dtype')
    if fields:
        ## error: column name missing
        field_diff = list(set([i['name'] for i in fields]) - set(df.columns))
        if field_diff:
            messages.error(request, 'ERROR: Column {} missing, please check input file'.format(', '.join(field_diff)))
            return cxt
    else:
        messages.error(request, 'SYSTEM ERROR: No field detected for requested template')
        return cxt

    # check column data type
    err_cnt = 0
    for f in fields:
        name, dtype = f['name'], f['dtype']
        if dtype in ['NUMERIC', 'DATETIME']:
            col = df[name].copy()
            nan_idx = col.isnull() # NaN index in orginal column
            if dtype == 'NUMERIC':
                if col.str.contains(r'\s|,|\$').sum() > 0:
                    messages.warning(request, 'WARNING: Column {} contains space/comma/dollar'.format(name))
                    col = col.str.replace(r'\s|,|\$', '')
                col = pd.to_numeric(col.fillna(0), errors='coerce')
            else: # DATETIME
                col = pd.to_datetime(col.fillna(0), errors='coerce')
            if col.isnull().sum() > 0:
                row_num = list(col[col.isnull()].index+2) # idx and header: +2 to get excel row numbers
                row_num = ', '.join(str(x) for x in row_num)
                messages.error(request, 'ERROR: Column {} non {} rows: {}, please correct'.format(name, dtype.lower(), row_num))
                err_cnt += 1
            else: # to keep the original NaN values
                col[nan_idx] = None
                df[name] = col
    if err_cnt > 0:
        ## error: column can not be converted to specified type
        return cxt
    else:
        messages.success(request, 'SUCCESS: Column name and data type check passed')

    # check rule set
    rulesets = RuleSet.objects.filter(field__template=template).select_related('field', 'rule').all()
    if rulesets:
        quality = Quality(df, rulesets)
        output = quality.output()
        # generate and output quality check report
        if output['err_msg']:
            df_err = pd.DataFrame({'message': output['err_msg'], 'row_number': output['err_detail']})
            df_err['level'] = 'ERROR'
            df_wrn = pd.DataFrame({'message': output['wrn_msg'], 'row_number': output['wrn_detail']})
            df_wrn['level'] = 'WARNING'
            df_scs = pd.DataFrame({'message': output['scs_msg']})
            df_scs['level'] = 'SUCCESS'
            df_report = pd.concat([df_err, df_wrn, df_scs], sort=False)
            cxt['df_report'] = df_report.to_json(orient='records')
            cxt['clean'] = 'false'
        else:
            cxt['clean'] = 'ture'
            cxt['df_report'] = pd.DataFrame().to_json(orient='records')
        df_meta = df.describe(include='all').transpose()
        df_meta['num_null'] = df.isnull().sum()
        df_meta.reset_index(inplace=True)
        cxt['df_meta'] = df_meta[['index', 'count', 'unique', 'top', 'freq', 'mean', 'std', 'min', 'max', 'num_null']].to_json(orient='records')
        return cxt
    else:
        messages.error(request, 'SYSTEM ERROR: No rule detected for requested template')
        return cxt



    
    








