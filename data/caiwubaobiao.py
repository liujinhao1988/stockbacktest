import os
import pandas as pd

df =pd.read_csv('sh600001_financial_statements.csv')
print(df)

a =df.loc[183,['20081231']]

print(a)