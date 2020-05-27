import os
import pymongo
import pandas as pd
import json



client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['daily']
col=db['sz300611']


df=pd.read_csv('sz300611.csv')

col.insert_many(json.loads(df.T.to_json()).values())


def insert_data():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['daily']

    path = '/home/biedongpython/下载/zhangdieting'
    list = os.listdir(path)
    list.sort()

    for name in list:
        in_f='/home/biedongpython/下载/zhangdieting/{}'.format(name)
        db_name=name.rstrip('.csv')
        col = db[db_name]
        df = pd.read_csv(in_f)
        col.insert_many(json.loads(df.T.to_json()).values())

        
        print(db_name)


if __name__=='__main__':
    insert_data()

