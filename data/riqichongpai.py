#日期有倒序变正序
'''
打开时就设置索引
df= pd.read_csv('sh000300.csv',index_col=[1])
df.sort_index(inplace=True)
'''

import os
import pandas as pd

def sort_time():
    #path = '/home/biedongpython/下载/daily/index'
    path = '/home/biedongpython/下载/daily/stock'

    list = os.listdir(path)
    list.sort()

    for name in list:
        #in_f = '/home/biedongpython/下载/daily/index/{}'.format(name)
        #out_f = '/home/biedongpython/下载/sort_daily/index/{}'.format(name)

        in_f = '/home/biedongpython/下载/daily/stock/{}'.format(name)
        out_f = '/home/biedongpython/下载/sort_daily/stock/{}'.format(name)


        df = pd.read_csv(in_f, index_col=[1])
        df.sort_index(inplace=True)
        df.to_csv(out_f)

if __name__=='__main__':
    sort_time()