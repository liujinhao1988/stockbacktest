# _*_ coding:utf-8 _*_





import os

def xls_to_csv():
    name = ['BalanceSheet', 'CashFlow', 'ProfitStatement']
    #name = ['CashFlow']
    for nn in name:
        path = '/home/biedongpython/下载/caiwubaobiao/{}'.format(nn)
        list = os.listdir(path)
        list.sort()
        inputBS = path + '/{}'
        outBS = path.replace('caiwubaobiao', 'new') + '/{}'
        os.makedirs(outBS.rstrip('/{}'))
        for i in list:

            with open(outBS.format(i).replace('.xls', '.csv'), 'w') as b:

                f = open(inputBS.format(i), 'rb')
                lines = f.readlines()
                for line in lines:
                    line = str(line, encoding='gbk')
                    line = line.replace("\t", ",")
                    b.write(line)
                f.close()
            b.close()


def test():

    with open('b.csv', 'w') as b:
        f = open('sh600225_CashFlow.xls', 'rb')
        lines = f.readlines()
        i=0
        for line in lines:
            print(i)
            line = str(line, encoding='gbk')
            line = line.replace("\t", ",")
            b.write(line)
            i=i+1
        f.close()
    b.close()




if __name__=='__main__':
    test()

