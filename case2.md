# case 2：三根阳线改变信仰，使用DataView神器快速做研究

case 1 “初识A股”中，我们主要从宏观角度，看看中国资本市场的整体情况。

本案例中，我们通过一个有趣的例子，看看jaqs如何能帮助你快速进行个股量化研究。

从几个问题出发：（如果你想直接撸代码，请访问[这里](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case2.ipynb)）

股市中有一个流行的谚语叫做：“三根阳线改变信仰”，指的是如果某只个股出现了连续三天上涨，可能会开始一波行情。

这个说法是否靠谱，投资者可以有自己的判断。但一个更加基本的问题是，我们怎么能快速的识别出这样的个股呢？

jaqs自带的DataView数据处理神器，让您只要通过少数的几行代码，就能实现这个目标。

## 1. 三根阳线的定义

描述一只股票的价格，一般有OHLC(Open, High, Low, Close)这几个基本属性。

阳线的定义表述为两个条件：

+ close - open > 0，即收盘价大于开盘价
+ (close - open) / (high - low) >= 0.7，即收盘价与开盘价的差，比最高价与最低价的差，至少超过70%

这里面的0.7其实是一个参数，也可以严格到0.9或者放松到0.4，这一般会改变阳线的形状。

如下图所示，是几个典型的阳线：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case2-1.png)

## 2. 利用DataView快速计算阳线

直接上代码，如下：
```python
from jaqs.data import RemoteDataService, DataView

data_config = {
    "remote.data.address": "tcp://data.tushare.org:8910",
    "remote.data.username": "phone",
    "remote.data.password": "token"
}

UNIVERSE = '000300.SH'

start_date = 20171201
curr_date = 20171212

dataview_props = {
    # Start and end date of back-test
    'start_date': start_date, 'end_date': curr_date,
    # Investment universe and performance benchmark
    'universe': UNIVERSE, 'benchmark': '000300.SH',
    # Data fields that we need
    'fields': 'close,open,high,low',
    # freq = 1 means we use daily data. Please do not change this.
    'freq': 1
}

# RemoteDataService communicates with a remote server to fetch data
ds = RemoteDataService()
# Use username and password in data_config to login
ds.init_from_config(data_config)

# DataView utilizes RemoteDataService to get various data and store them
dv = DataView()
dv.init_from_config(dataview_props, ds)
dv.prepare_data()

# add formula to calculate three yang k line
dv.add_formula('is_yang', '(close > open) && ( (close - open) / (high - low) >= 0.7)', is_quarterly=False)
dv.add_formula('three_yang', 'is_yang && Delay(is_yang, 1) && Delay(is_yang, 2)', is_quarterly=False)

# get the result
df = dv.get_snapshot(curr_date)
df[df['three_yang'] == 1.0]

```

## 3. 结果分析

我们发现，当参数设置成0.7时，在20171212当天无法找到满足条件的股票，但如果把参数放宽到0.45，就可以找到三只这样的股票。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case2-2.png)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case2-3.png)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case2-4.png)

观察上述三只股票在2017年12月13日的走势，发现有两支下跌，一只上涨。

用这种方法是否可以赚钱，应该还需要打一个问号。

这个例子只是简单的秀了一下DataView，其实这只是它全部功能的百分之一。

DataView的详细使用说明，请参考[这里](https://github.com/quantOS-org/JAQS/blob/master/doc/data_view.md)

## 4. 想尝试一下？

请访问www.quantos.org，下载安装JAQS，开始自己的量化旅程吧。

这里的东西都是开源和免费的。


