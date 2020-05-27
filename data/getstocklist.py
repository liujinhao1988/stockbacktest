
import os


path = '/home/biedongpython/下载/zhangdieting'
list = os.listdir(path)
list.sort()

stocklist=[]

for name in list:
    stockname = name.rstrip('.csv')
    stocklist.append(stockname)

print(stocklist)