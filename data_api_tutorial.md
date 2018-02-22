
# 聊聊quantos数据

quantos为量化研究提供一站式的解决方案，这篇文章里，我们聊一下quantos提供的数据服务。

## 整体架构

![](https://raw.githubusercontent.com/PKUJohnson/LearnJaqsByExample/master/image/quantos_data.png)

目前quantos提供的数据包括：

+ 基础数据，主要是一些基础信息，包括证券信息、行业代码、指数信息、交易日历等。
+ 市场数据，即由市场行情产生的数据，包括实时行情、实时分钟线、历史tick、历史日线、历史分钟线等。
+ 参考数据，包括股票的复权因子、分红、停复牌、行业分类，指数的成份股，公募基金的净值等。


## 数据获取

使用DataApi，可以获取quantos提供的各种研究数据。使用前需要先登录，代码如下：



```python
import os
from jaqs.data import DataApi
api   = DataApi(addr="tcp://data.quantos.org:8910")
phone = os.environ.get("QUANTOS_USER")
token = os.environ.get("QUANTOS_TOKEN")
df, msg = api.login(phone, token)
print(df, msg)
```

### 市场数据

市场数据分为实时数据和历史数据，通过几个不同的接口来获取。

#### 实时行情快照

通过quote函数，可以查询多只证券的实时行情快照。

```python
df, msg = api.quote(
	symbol="000001.SH, cu1709.SHF", 
	fields="open,high,low,last,volume"
)
df.head(10)
```

#### 实时行情订阅

通过subscribe函数，可以订阅多只证券的实时行情，通过回调on_quote函数，将最新的数据返回给用户。

```python
def on_quote(k,v):
    print(v['symbol']) // 标的代码
    print(v['last'])   // 最新成交价
    print(v['time'])   // 最新成交时间

subs_list,msg = api.subscribe("000001.SH, cu1709.SHF",func=on_quote,fields="symbol,last,time,volume")
print(subs_list, msg)
```

quantos实时行情数据包括：

+ 股票level1行情，每3.0秒刷新一次
+ 期货level1行情，每0.5秒刷新一次

实时行情数据主要包括：

+ 时间信息(date, time, trade_date)
+ 最新的OHLC(open, high, low, close）
+ 最新的盘口信息（ask1-ask5, bid1-bid5）
+ 成交统计信息volume, turnover, vwap
+ 静态信息，包括涨停价、跌停价、昨收价、昨结算价

#### 分钟线查询

分钟线是将实时行情数据按照分钟为单位进行统计分析，得到的信息

bar函数查询分钟线信息，quantos支持1M、5M、15M三种分钟线，trade_date=0时，查询的是当日的分钟线，否则查询的是历史分钟线。

```python
df,msg = api.bar(
	symbol="600030.SH", 
	trade_date=20170928, 
	freq="5M",
	start_time=0,
	end_time=160000,
	fields=""
)
df.head(10)
```

quantos每日根据接收的tick数据，合成分钟线并保存在文件中。

分钟线数据主要包括：

+ 时间信息(date, time, trade_date)
+ 这一分钟的OHLC(open, high, low, close）
+ 这一分钟内最后的盘口信息（ask1-ask5, bid1-bid5）
+ 成交统计信息volume, turnover, vwap

很多交易策略是基于分钟线进行研究的，因为分钟线的统计规律更加稳定。

#### 日线查询

日线，顾名思义就是每日收盘数据。属于日级别的低频数据，很多股票alpha策略都是在日线上进行研究的。

```python
df, msg = api.daily(
	symbol="600832.SH, 600030.SH", 
	start_date=20121026,
	end_date=20121130, 
	fields="", 
	adjust_mode="post"
)
df.head(10)
```

daily函数可以获取多只证券某段时间内的每日收盘数据，adjust_mode字段是复权方式，这就涉及到股票价格复权的问题。

那股票复权是咋回事呢？

原来，很多股票每年都会进行分红、配股等操作，会导致股票的价格发生突变。比如：

+ 某股票今日日终分红每股1元，则次日其股价自动减少1元。
+ 某股票今日日终实施配股(或送股)，每股配(送)2股，则次日股价自动调整为今日收盘价的1/3.

还有一些股票是分红和配股(送股)一起实施。

复权就是按照红利再投资的原则，复原真实的股价，即在最新的股价上乘以一个复权因子的系数。

复权可以解决股票长周期回测的价格问题。

### 通用数据查询接口


除市场数据外，基础数据和参考数据都是通过一个叫做query的通用数据查询接口api获取的，样例代码如下：


```python
# 通用数据查询接口样例
df, msg = api.query(
    view="jz.instrumentInfo", 
    fields="status,list_date, fullname_en, market", 
    filter="inst_type=1&status=1&symbol="
)
df.head(10)
```

这里面有三个参数：
+ 第一个参数view需填入对应的接口名
+ 输入参数指的是filter参数里面的内容，通过'&'符号拼接
+ 输出参数指的是fields里面的内容，通过','隔开

也就是说，使用query接口，你需要提供三个信息，接口名、条件参数、输出字段

问题来了，如何知道有哪些接口呢？如何知道每个接口有哪些输入参数和输出参数可选择呢？

彩蛋来了，有两个查询接口信息的接口。help.apiList，help.apiParam

```python
# 查询有哪些接口可以调用
df, msg = api.query(
    view="help.apiList", 
    fields="", 
    filter=""
)
df.head(100)
```

```python
# 查询jz.instrumentInfo接口的输入输出参数
df, msg = api.query(
    view="help.apiParam", 
    fields="", 
    filter="api=jz.instrumentInfo"
)
df.head(100)
```

### 基础数据

+ 证券基础信息
+ 交易日历信息
+ 指数基本信息
+ 行业信息


```python
# 证券基础信息

df, msg = api.query(
    view="jz.instrumentInfo", 
    fields="", 
    filter="inst_type=1&status=1&symbol="
)
df.head(10)
```

```python
# 指数基本信息

df, msg = api.query(
    view="lb.indexInfo", 
    fields="", 
    filter=""
)
df.head(10)
```

```python
# 交易日历信息，只支持中国的交易日历

df, msg = api.query(
    view="jz.secTradeCal", 
    fields="", 
    filter=""
)
df.head(10)
```


```python
# 行业代码表

df, msg = api.query(
    view="lb.industryType", 
    fields="", 
    filter="industry_src=SW&level=1"
)
df.head(100)
```

上面样例获取的是申万一级行业分类代码，一共28个一级行业。

### 参考数据

股票相关

+ 股票分红配股数据
+ 股票停复牌数据
+ 股票复权因子数据
+ 股票行业分类数据

指数相关

+ 指数成分股

基金相关

+ 公募基金净值


```python
# 股票分红配股数据

df, msg = api.query(
    view="lb.secDividend", 
    fields="", 
    filter="symbol=600036.SH"
)
df.head(100)
```

```python
# 股票停复牌数据

df, msg = api.query(
    view="lb.secSusp", 
    fields="", 
    filter="symbol=600036.SH"
)
df.head(100)
```

```python
# 股票复权因子数据

df, msg = api.query(
    view="lb.secAdjFactor", 
    fields="", 
    filter="symbol=600036.SH"
)
df.tail(100)
```

```python
# 股票行业分类数据

df, msg = api.query(
    view="lb.secIndustry", 
    fields="", 
    filter="symbol=600030.SH,600031.SH&industry_src=SW"
)
df.tail(100)
```

```python
# 指数成份股数据

df, msg = api.query(
    view="lb.indexCons", 
    fields="", 
    filter="index_code=000016.SH&start_date=20170101&end_date=20171229"
)
df.tail(100)
```

指数成份股接口的正确用法是，系统返回了在start_date和end_date之间所有日期相关的记录。

用户如果要查询某一天的指数成份股，将start_date和end_date设置成一样就可以了。

```python
# 指数成份股数据（某一天）

df, msg = api.query(
    view="lb.indexCons", 
    fields="", 
    filter="index_code=000016.SH&start_date=20180221&end_date=20180221"
)
df.tail(100)
```

```python
# 公募基金净值

df, msg = api.query(
    view="lb.mfNav", 
    fields="", 
    filter="symbol=510050.SH&start_pdate=20170101&end_pdate=20180101"
)
df
```

