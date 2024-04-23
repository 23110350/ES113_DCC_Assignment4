!pip install tabula-py pandas
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

pdf_path = 'C:\Users\sony\Desktop\DCC_App\PDF Files\EB_Purchase_Details.pdf'
data_array = pdf_to_array(pdf_path)

print(data_array)
columns = ['Sr No.', 'Reference No (URN)', 'Journal Date', 'Date of Purchase', 'Date of Expiry',
           'Name of the Purchaser', 'Prefix', 'Bond Number', 'Denominations', 'Issue Branch Code',
           'Issue Teller', 'Status']

df2 = pd.DataFrame(data_array, columns=columns)

df2['Issue Branch Code'] = df2['Issue Branch Code'].apply(lambda x: str(x).zfill(5))
df2.to_csv('EB_Purchase_Details.csv', index=False)