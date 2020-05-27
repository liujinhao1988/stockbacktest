#获取某日的所有股票信息，剔除非交易日，涨停版
from model.util.stocklist import stocklist
from model.database import db_daily
import pandas as pd



def get_bar(day):
    list=[]
    for name in stocklist:
        col = db_daily[name]
        result = col.find_one({'date': day})
        df1 = pd.DataFrame(result, index=[0])
        list.append(df1)

    df=pd.concat(list,axis=0,sort=False)
    del df['_id']

    df.dropna(subset=['code'],inplace=True)

    return df







