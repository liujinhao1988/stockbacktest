import pandas as pd
import os
df=pd.read_csv('sh600008_financial_statements.csv')

df=df.loc[:, ~df.columns.str.contains('^Unnamed')]

df.to_csv('a.csv',index=False)


def deleteunnamed():
    path='/home/biedongpython/下载/hebing'
    list = os.listdir(path)
    list.sort()

    for name in list:
        in_f='/home/biedongpython/下载/hebing/{}'.format(name)
        out_f='/home/biedongpython/下载/caiwubaobiaozuihou/{}'.format(name)
        df=pd.read_csv(in_f)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(out_f, index=False)


if __name__=='__main__':
    deleteunnamed()