
# quantos数据之数字货币篇

为了满足广大数字货币交易者的需求，quantos重磅推出数字货币数据接口。本文详述如何获取和使用。

## 数据框架

quantos提供的数字货币数据包括：

+ 精选十大数字货币：选取了目前市值最大的10大数字货币。
+ 精选十大交易所：目前最活跃的十大数字货币交易所。
+ 精选106对数字货币交易对：包括币币交易/数字货币与法币交易等交易对。
+ 提供每日的行情数据，包含全部历史。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc.png)

## 数据获取

使用DataApi，可以获取quantos提供的数字数据。使用前需要先登录，代码如下：

```python
import os
from jaqs.data import DataApi
api   = DataApi(addr="tcp://data.quantos.org:8910")
phone = os.environ.get("QUANTOS_USER")
token = os.environ.get("QUANTOS_TOKEN")
df, msg = api.login(phone, token)
print(df, msg)
```

### 获取交易所信息(dcExchangeInfo)
```python
df, msg = api.query(view ="lb.dcExchangeInfo")
df.head(10)
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc_exchange.png)

### 获取数字货币信息(lb.dcCoinInfo)
```python
df, msg = api.query(view ="lb.dcCoinInfo")
df.head(10)
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc_coin.png)

### 获取数字货币交易对信息(lb.dcTradeInfo)
```python
df, msg = api.query(view ="lb.dcTradeInfo")
df.head(10)
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc_inst.png)

### 获取数字货币日行情信息(lb.dcDaily)

```python
df,msg = api.query(view ="lb.dcDaily",filter="symbol=bitcoin:usd:bitfinex&start_date=20180101&end_date=20180515", fields="open,high,low,volume,turnover")
df.head(10)
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc_daily.png)

### 一个简单应用

我们选取各交易所的比特币/美元交易对，画出2018年以来的走势，代码如下：

```python
symbol_list = [
	"bitcoin:usd:bitfinex",
	"bitcoin:usd:gdax",
]

symbols = ",".join(symbol_list)

import datetime
df,msg = api.query(view ="lb.dcDaily",filter="symbol="+symbols+"&start_date=20180101&end_date=20180515", fields="close")
df['trade_date'] = df['trade_date'].apply(lambda x : datetime.datetime.strptime(x, "%Y%m%d"))
df = df.pivot(index='trade_date', columns='symbol', values='close')

df.plot(figsize=(16,10))
```

结果是这样的：
![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/dc_example.png)


## 结束语

欢迎大家登录quantos网站，下载金融终端，体验数字货币的数量化分析的乐趣。

Welcome join us.


