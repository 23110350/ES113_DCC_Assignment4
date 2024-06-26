import tabula
import pandas as pd
import numpy as np

def clean_data(df):
    df = df.dropna(how='all')
    df.columns = df.columns.str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace('', np.nan)
    df = df.dropna()
    return df

def pdf_to_array(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    df = pd.concat(tables)
    df = clean_data(df)
    data_array = df.values
    return data_array

pdf_path = 'C:\Users\sony\Desktop\DCC_App\PDF Files\EB_Redemption_Details.pdf'
data_array = pdf_to_array(pdf_path)

columns = ['Sr No.', 'Date of Encashment', 'Name of the Political Party',
           'Account no. of Political Party', 'Prefix', 'Bond Number',
           'Denominations', 'Pay Branch Code', 'Pay Teller']

df1 = pd.DataFrame(data_array, columns=columns)

df1['Pay Branch Code'] = df1['Pay Branch Code'].apply(lambda x: str(x).zfill(5))
df1['Pay Branch Code'] = df1['Pay Branch Code'].apply(lambda x: str(x))
df1.to_csv('EB_Redemption_Details.csv', index=False)
