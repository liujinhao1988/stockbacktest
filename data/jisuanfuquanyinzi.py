import os
import pandas as pd
import numpy as np
import time

#回报因子，涨跌停，对应的财报日期
df=pd.read_csv('sh600065.csv')
time_start=time.time()

#涨停
df['limit_up']=None

#跌停
df['limit_down']=None
#财报日期financial statements
df['financial_statements']=None
#回报因子
df['return_factor']=None

df.loc[df['change']>=0.095,'limit_up']=1
df.loc[df['change']<0.095,'limit_up']=0

df.loc[df['change']<=-0.095,'limit_down']=1
df.loc[df['change']>-0.095,'limit_down']=0

df.loc[(df['date']>=20160501)&(df['date']<20170501),'financial_statements']=20151231
df.loc[(df['date']>=20150501)&(df['date']<20160501),'financial_statements']=20141231
df.loc[(df['date']>=20140501)&(df['date']<20150501),'financial_statements']=20131231
df.loc[(df['date']>=20130501)&(df['date']<20140501),'financial_statements']=20121231
df.loc[(df['date']>=20120501)&(df['date']<20130501),'financial_statements']=20111231
df.loc[(df['date']>=20110501)&(df['date']<20120501),'financial_statements']=20101231
df.loc[(df['date']>=20100501)&(df['date']<20110501),'financial_statements']=20091231
df.loc[(df['date']>=20090501)&(df['date']<20100501),'financial_statements']=20081231
df.loc[(df['date']>=20080501)&(df['date']<20090501),'financial_statements']=20071231
df.loc[(df['date']>=20070501)&(df['date']<20080501),'financial_statements']=20061231
df.loc[(df['date']>=20060501)&(df['date']<20070501),'financial_statements']=20051231
df.loc[(df['date']>=20050501)&(df['date']<20060501),'financial_statements']=20041231
df.loc[(df['date']>=20040501)&(df['date']<20050501),'financial_statements']=20031231
df.loc[(df['date']>=20030501)&(df['date']<20040501),'financial_statements']=20021231
df.loc[(df['date']>=20020501)&(df['date']<20030501),'financial_statements']=20011231
df.loc[(df['date']>=20010501)&(df['date']<20020501),'financial_statements']=20001231
df.loc[(df['date']>=20000501)&(df['date']<20010501),'financial_statements']=19991231
df.loc[(df['date']>=19990501)&(df['date']<20000501),'financial_statements']=19981231
df.loc[(df['date']>=19980501)&(df['date']<19990501),'financial_statements']=19971231
df.loc[(df['date']>=19970501)&(df['date']<19980501),'financial_statements']=19961231
df.loc[(df['date']>=19960501)&(df['date']<19970501),'financial_statements']=19951231
df.loc[(df['date']>=19950501)&(df['date']<19960501),'financial_statements']=19941231
df.loc[(df['date']>=19940501)&(df['date']<19950501),'financial_statements']=19931231
df.loc[(df['date']>=19930501)&(df['date']<19940501),'financial_statements']=19921231
df.loc[(df['date']>=19920501)&(df['date']<19930501),'financial_statements']=19911231

df['log_adjust']=np.log(df.adjust_price)
df['adjust_return']=df.log_adjust.diff()
df.loc[0,'adjust_return']=0.0
df['return_factor']=np.exp(df['adjust_return'])


del df['log_adjust']
del df['adjust_return']
# num=df.shape[0]
# for i in range(1,num):
#     df.loc[i,'return_factor']=df.loc[i,'adjust_price']/df.loc[i-1,'adjust_price']

df.to_csv('a.csv',index=False)
time_end=time.time()
print(time_end-time_start)

def cal_return_factor():
    path = '/home/biedongpython/下载/fillna'
    list = os.listdir(path)
    list.sort()

    for name in list:
        in_f='/home/biedongpython/下载/fillna/{}'.format(name)
        out_f='/home/biedongpython/下载/zhangdieting/{}'.format(name)

        df = pd.read_csv(in_f)


        # 涨停
        df['limit_up'] = None

        # 跌停
        df['limit_down'] = None
        # 财报日期financial statements
        df['financial_statements'] = None
        # 回报因子
        df['return_factor'] = None

        df.loc[df['change'] >= 0.095, 'limit_up'] = 1
        df.loc[df['change'] < 0.095, 'limit_up'] = 0

        df.loc[df['change'] <= -0.095, 'limit_down'] = 1
        df.loc[df['change'] > -0.095, 'limit_down'] = 0

        df.loc[(df['date'] >= 20160501) & (df['date'] < 20170501), 'financial_statements'] = 20151231
        df.loc[(df['date'] >= 20150501) & (df['date'] < 20160501), 'financial_statements'] = 20141231
        df.loc[(df['date'] >= 20140501) & (df['date'] < 20150501), 'financial_statements'] = 20131231
        df.loc[(df['date'] >= 20130501) & (df['date'] < 20140501), 'financial_statements'] = 20121231
        df.loc[(df['date'] >= 20120501) & (df['date'] < 20130501), 'financial_statements'] = 20111231
        df.loc[(df['date'] >= 20110501) & (df['date'] < 20120501), 'financial_statements'] = 20101231
        df.loc[(df['date'] >= 20100501) & (df['date'] < 20110501), 'financial_statements'] = 20091231
        df.loc[(df['date'] >= 20090501) & (df['date'] < 20100501), 'financial_statements'] = 20081231
        df.loc[(df['date'] >= 20080501) & (df['date'] < 20090501), 'financial_statements'] = 20071231
        df.loc[(df['date'] >= 20070501) & (df['date'] < 20080501), 'financial_statements'] = 20061231
        df.loc[(df['date'] >= 20060501) & (df['date'] < 20070501), 'financial_statements'] = 20051231
        df.loc[(df['date'] >= 20050501) & (df['date'] < 20060501), 'financial_statements'] = 20041231
        df.loc[(df['date'] >= 20040501) & (df['date'] < 20050501), 'financial_statements'] = 20031231
        df.loc[(df['date'] >= 20030501) & (df['date'] < 20040501), 'financial_statements'] = 20021231
        df.loc[(df['date'] >= 20020501) & (df['date'] < 20030501), 'financial_statements'] = 20011231
        df.loc[(df['date'] >= 20010501) & (df['date'] < 20020501), 'financial_statements'] = 20001231
        df.loc[(df['date'] >= 20000501) & (df['date'] < 20010501), 'financial_statements'] = 19991231
        df.loc[(df['date'] >= 19990501) & (df['date'] < 20000501), 'financial_statements'] = 19981231
        df.loc[(df['date'] >= 19980501) & (df['date'] < 19990501), 'financial_statements'] = 19971231
        df.loc[(df['date'] >= 19970501) & (df['date'] < 19980501), 'financial_statements'] = 19961231
        df.loc[(df['date'] >= 19960501) & (df['date'] < 19970501), 'financial_statements'] = 19951231
        df.loc[(df['date'] >= 19950501) & (df['date'] < 19960501), 'financial_statements'] = 19941231
        df.loc[(df['date'] >= 19940501) & (df['date'] < 19950501), 'financial_statements'] = 19931231
        df.loc[(df['date'] >= 19930501) & (df['date'] < 19940501), 'financial_statements'] = 19921231
        df.loc[(df['date'] >= 19920501) & (df['date'] < 19930501), 'financial_statements'] = 19911231

        df['log_adjust'] = np.log(df.adjust_price)
        df['adjust_return'] = df.log_adjust.diff()
        df.loc[0, 'adjust_return'] = 0.0
        df['return_factor'] = np.exp(df['adjust_return'])

        del df['log_adjust']
        del df['adjust_return']








        df.to_csv(out_f, index=False)


if __name__=='__main__':
    cal_return_factor()


