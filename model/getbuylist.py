import pandas as pd
#获取要购买的股票列表
def get_buy_list(df,stocknum):
    all_stock=list(df['atlast'])
    n=len(all_stock)

    all_stock.sort()#shexu
    head=all_stock[stocknum]
    tail=all_stock[n-stocknum-1]

    df_head=df[df.atlast<head]
    df_tail=df[df.atlast>tail]

    list_head=list(df_head['code'])
    list_tail=list(df_tail['code'])

    return list_head,list_tail