import numpy as np
import pandas as pd



#fama-french 三因子模型实现 beta值，市净率，总市值
#开始日期
first_date=20100101
#结束日期
last_date= 20161231
#调仓频率
frq=60
#持仓数量
stocknum=50
#起始资金
money=100000000.00

def before_trade(df):
    pass

#策略逻辑
def handle_bar(df):


    #删除空值
    df.dropna(subset=['PB'],inplace=True)
    df.dropna(subset=['beta'], inplace=True)
    df.dropna(subset=['market_value'], inplace=True)
    #删除负值
    df=df[df.PB > 0]
    df=df[df.beta > 0]
    #求市值的对数值
    df['log_market_value']=np.log(df.market_value)
   


    # 合成选股指标
    df['atlast']=df['PB']+df['beta']+df['log_market_value']


    return df



