# stockbacktest
====


#项目简介
-------
这个项目是一个股票策略回测程序<br>

所使用的技术为python和mongodb<br>

data文件夹中主要包含数据的抓取，处理，存储方面的脚本<br>

tests文件夹包含测试函数<br>

model包含回测引擎的基础模块<br>

examples包含了策略例子<br>

output中包含回测结果<br>

output中的图片下载后可以显示<br>

#项目使用
-------

先运行data文件夹中的datacunchu.py将数据导入mongodb（由于数据体积过大暂时没有上传）<br>

在examples文件夹中写好策略逻辑<br>
![carbon](https://github.com/user-attachments/assets/d6e3184e-63e4-4cea-872b-de7afc462d60)

然后在backtest.py导入策略名称<br>

即from examples import threefactors as strategy<br>

运行backtest.py即可获得回测结果<br>

图片中红线为策略走势，以中证1000的走势为参照标准<br>
![毛利减销管取大](https://github.com/user-attachments/assets/bea1469d-04c0-42fd-960e-dbc463a093d9)
