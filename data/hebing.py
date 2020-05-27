import os
import pandas as pd
def annualreports(in_f):
    d_f = pd.read_csv(in_f)
    for i in range(1985, 2019, 1):
        try:
            d_f = d_f.drop('{}0331'.format(i), axis=1)
        except KeyError:
            pass
    for i in range(1985, 2019, 1):
        try:
            d_f = d_f.drop('{}0630'.format(i), axis=1)
        except KeyError:
            pass
    for i in range(1985, 2019, 1):
        try:
            d_f = d_f.drop('{}0930'.format(i), axis=1)
        except KeyError:
            pass
    return d_f

#获取股票列表
path = '/home/liujinhao/data/trading-data_full.20170228/stock data'
list = os.listdir(path)
stocklist=[]
for i in list:
    stocklist.append(i.rstrip('.csv'))




for name in stocklist:
    in_f1 = '/home/liujinhao/data/new/{}_BalanceSheet.csv'.format(name)
    in_f2 = '/home/liujinhao/data/new/{}_CashFlow.csv'.format(name)
    in_f3 = '/home/liujinhao/data/new/{}_ProfitStatement.csv'.format(name)
    out_f = '/home/liujinhao/data/hebing/{}.csv'.format(name)
    d_f1 = annualreports(in_f1)
    d_f2 = annualreports(in_f2)
    d_f3 = annualreports(in_f3)
    df = pd.concat([d_f1, d_f2, d_f3], axis=0, sort=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv(out_f, index=False)