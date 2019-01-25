import pandas as pd
from .models import Template, Field, Rule, RuleSet

def check_quality(input_file, template_id):
    # input_file: request.FILES['upload']
    file_name = input_file.name
    err_cnt = 0
    wrn_cnt = 0

    if ".xlsx" in file_name:
        # determine sheet to use
        xl = pd.ExcelFile(input_file)
        sheet_name = 0
        if len(xl.sheet_names) > 1:
            print('oops')
        else:
            df = pd.read_excel(xl, sheet_name=0, dtype=object)
    else:
        df = pd.read_csv(input_file, header=None, low_memory=False)
    print(df.head())