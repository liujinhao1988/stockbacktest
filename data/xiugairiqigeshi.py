#转化日期格式

import os
import pandas as pd

'''
df= pd.read_csv('sz300617.csv')

df['date'] = df['date'].map(lambda x:x.replace('-','',2))
a=df['date'][0]
b=a.replace('-','',2)

'''
def trans_time():

    path = '/home/biedongpython/下载/trading-data_full.20170228/stock data'

    #path = '/home/biedongpython/下载/trading-data_full.20170228/index data'

    list = os.listdir(path)
    list.sort()

    for name in list:
        in_f='/home/biedongpython/下载/trading-data_full.20170228/stock data/{}'.format(name)
        out_f='/home/biedongpython/下载/daily/stock/{}'.format(name)

        #in_f = '/home/biedongpython/下载/trading-data_full.20170228/index data/{}'.format(name)
        #out_f = '/home/biedongpython/下载/daily/index/{}'.format(name)

        df = pd.read_csv(in_f)
        df['date'] = df['date'].map(lambda x: x.replace('-', '', 2))




        df.to_csv(out_f, index=False)


if __name__=='__main__':
    trans_time()


