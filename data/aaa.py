import pandas as pd
path = '../../../../桌面/calenda.csv'
f = open(path, 'r')
content = f.read()
list = []
rows = content.split('\n')
for row in rows:
    list.append(row.split(','))

f.close()

aaa = []
for i in list:
    aaa.append(i[0])
aaa=aaa[0:-1]

bbb=[]
for i in aaa:
    m=int(i)
    bbb.append(m)


print(bbb)
# print(type(c))
#
#
# df=pd.read_csv('sh600001.csv')
#
# m=df.at[12,'date']
# print(m)
# print(type(m))

