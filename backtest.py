#导入策略threefactors
from examples import threefactors as strategy

from model.utils.stocklist import stocklist
from model.utils import tradingdate
from model.database import db_daily
from model.getbar import get_bar
from model.getbuylist import get_buy_list
from model.get_return_factor import get_return_factor


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

day_list=tradingdate.get_day_list(strategy.first_date,strategy.last_date)
trade_date=tradingdate.get_trade_date(strategy.first_date,strategy.last_date,strategy.frq)
buy_dict_head={}
buy_dict_tail={}

for date in trade_date:
    df=get_bar(date)
    df=strategy.handle_bar(df)
    list_head, list_tail=get_buy_list(df,strategy.stocknum)
    buy_dict_head[date]=list_head
    buy_dict_tail[date]=list_tail
    print(date)


print('day_list')
print(day_list)
print('trade_date')
print(trade_date)
print('buy_dict_head')
print(buy_dict_head)
print('buy_dict_tail')
print(buy_dict_tail)




day_to_buylist_head={}
day_to_buylist_tail={}
for i in day_list:
    num_temp=list(filter(lambda x:x<=i,trade_date))
    a = max(num_temp)
    day_to_buylist_head[i] = buy_dict_head[a]
    day_to_buylist_tail[i]=buy_dict_tail[a]


account_dict_head={}
account_dict_tail={}

account_value_head={}
account_value_tail={}

account_value_head[day_list[0]]=strategy.money
account_value_tail[day_list[0]]=strategy.money


day_list_num=len(day_list)

for i in range(1,day_list_num):

   
    head_last=account_value_head[day_list[i-1]]
    return_head=get_return_factor(day_to_buylist_head(day_list[i]))
    account_value_head[day_list[i]]=head_last*return_head
	
   
    tail_last=account_value_tail[day_list[i-1]]
    return_tail=get_return_factor(day_to_buylist_tail(day_list[i]))
    account_value_tail[day_list[i]]=tail_last*return_tail



print('account_values_head')
print(account_value_head)
print('account_values_tail')
print(account_value_tail)

y_value_head=[]
y_value_tail=[]
for i in day_list:

    y_value_head.append(account_value_head[i]/strategy.money)
    y_value_tail.append(account_value_tail[i] / strategy.money)

x_values=[]
x=0
for i in day_list:
    x=x+1
    x_values.append(x)


df=pd.read_csv('hs300.csv',index_col=[0])
hs300_dict={}
start_day=df.loc[day_list[0],'close']
for date in day_list:
    a=df.loc[date,'close']
    b=a/start_day
    hs300_dict[date]=b
y_value_hs300=[]
for i in day_list:
    y_value_hs300.append(hs300_dict[i])


df=pd.read_csv('zz500.csv',index_col=[0])
zz500_dict={}
start_day=df.loc[day_list[0],'close']
for date in day_list:
    a=df.loc[date,'close']
    b=a/start_day
    zz500_dict[date]=b
y_value_zz500=[]
for i in day_list:
    y_value_zz500.append(zz500_dict[i])



df=pd.read_csv('zz1000.csv',index_col=[0])
zz1000_dict={}
start_day=df.loc[day_list[0],'close']
for date in day_list:
    a=df.loc[date,'close']
    b=a/start_day
    zz1000_dict[date]=b
y_value_zz1000=[]
for i in day_list:
    y_value_zz1000.append(zz1000_dict[i])


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x_values,y_value_head, color='r', label='strategy_head')
ax.plot(x_values,y_value_tail, color='b', label='strategy_tail')

ax.plot(x_values,y_value_hs300, color='green', label='hs300')
ax.plot(x_values,y_value_zz500, color='black', label='zz500')
ax.plot(x_values,y_value_zz1000, color='yellow', label='zz1000')



print('沪深300回报率'+str((y_value_hs300[-1]-1)*100)+'%')
print('中证500回报率'+str((y_value_zz500[-1]-1)*100)+'%')
print('中证1000回报率'+str((y_value_zz1000[-1]-1)*100)+'%')
print('head回报率'+str((y_value_head[-1]-1)*100)+'%')
print('tail回报率'+str((y_value_tail[-1]-1)*100)+'%')

plt.legend()
plt.show()
