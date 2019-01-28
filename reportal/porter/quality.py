import pandas as pd
from .models import Template, Field, Rule, RuleSet
from django.contrib import messages


def check_quality(request, input_file, template_id):
    # input_file: request.FILES['upload']
    file_name = input_file.name
    err_cnt = 0
    wrn_cnt = 0
    cxt = {}
    df = pd.DataFrame()

    # read file
    if ".xlsx" in file_name:
        xl = pd.ExcelFile(input_file)
        ## error: only 1 sheet allowed
        if len(xl.sheet_names) > 1:
            messages.error(request, 'Please only include one sheet in the excel file')
            return cxt
        else:
            df = pd.read_excel(xl, sheet_name=0, dtype=object)
    else:
        df = pd.read_csv(input_file, dtype=object)
    
    # check column name
    fields = Field.objects.filter(template=template_id).values('name', 'dtype')
    ## error: column name missing
    field_diff = list(set([i['name'] for i in fields]) - set(df.columns))
    if field_diff:
        messages.error(request, 'Column <{}> missing, please check input file'.format(', '.join(field_diff)))
        return cxt

    # check column data type
    for f in fields:
        name, dtype = f['name'], f['dtype']
        if dtype in ['NUMERIC', 'DATETIME']:
            col = df[name].copy()
            if dtype == 'NUMERIC':
                col = col.str.replace(r'\s|,|\$|(not set)|#N/A|nan', '')
                col = pd.to_numeric(col.fillna(0), errors='coerce')
            else: # DATETIME
                col = pd.to_datetime(col.fillna(0), errors='coerce')
            if sum(col.isnull()) > 0:
                row_ids = list(col[col.isnull()].index+1)
                messages.error(request, 'Column <{}> non {} rows: {}, please correct'.format(name, dtype.lower(), row_ids))
                err_cnt += 1
            else: # to keep the original NaN values
                if dtype == 'NUMERIC':
                    df[name] = col.str.replace(r'\s|,|\$|(not set)|#N/A|nan', '')
                    df[name] = pd.to_numeric(df[name], errors='coerce')
                else: # DATETIME
                    df[name] = pd.to_datetime(df[name], errors='coerce')
    if err_cnt > 0:
        return cxt

    
    








