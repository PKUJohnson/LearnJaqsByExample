
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

    username: 18612562791 0,
    

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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>high</th>
      <th>last</th>
      <th>low</th>
      <th>open</th>
      <th>symbol</th>
      <th>time</th>
      <th>volume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>000001.SH</th>
      <td>20180222</td>
      <td>3269.9156</td>
      <td>3268.5589</td>
      <td>3234.1152</td>
      <td>3237.5692</td>
      <td>000001.SH</td>
      <td>150052000</td>
      <td>138730445</td>
    </tr>
  </tbody>
</table>
</div>



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

    ['000001.SH', 'cu1709.SHF'] 0,
    

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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>close</th>
      <th>code</th>
      <th>date</th>
      <th>freq</th>
      <th>high</th>
      <th>low</th>
      <th>oi</th>
      <th>open</th>
      <th>settle</th>
      <th>symbol</th>
      <th>time</th>
      <th>trade_date</th>
      <th>turnover</th>
      <th>volume</th>
      <th>vwap</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>18.05</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.08</td>
      <td>18.00</td>
      <td>NaN</td>
      <td>18.01</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>93500</td>
      <td>20170928</td>
      <td>13576973.0</td>
      <td>752900.0</td>
      <td>18.032903</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18.03</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.06</td>
      <td>18.01</td>
      <td>NaN</td>
      <td>18.04</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>94000</td>
      <td>20170928</td>
      <td>16145566.0</td>
      <td>895110.0</td>
      <td>18.037522</td>
    </tr>
    <tr>
      <th>2</th>
      <td>18.04</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.05</td>
      <td>18.02</td>
      <td>NaN</td>
      <td>18.03</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>94500</td>
      <td>20170928</td>
      <td>11024829.0</td>
      <td>611400.0</td>
      <td>18.032105</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17.99</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.05</td>
      <td>17.97</td>
      <td>NaN</td>
      <td>18.04</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>95000</td>
      <td>20170928</td>
      <td>30021003.0</td>
      <td>1667190.0</td>
      <td>18.006948</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18.02</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.03</td>
      <td>17.97</td>
      <td>NaN</td>
      <td>17.98</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>95500</td>
      <td>20170928</td>
      <td>13691203.0</td>
      <td>761161.0</td>
      <td>17.987263</td>
    </tr>
    <tr>
      <th>5</th>
      <td>18.00</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.03</td>
      <td>17.98</td>
      <td>NaN</td>
      <td>18.01</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>100000</td>
      <td>20170928</td>
      <td>17562219.0</td>
      <td>975400.0</td>
      <td>18.005146</td>
    </tr>
    <tr>
      <th>6</th>
      <td>17.98</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.00</td>
      <td>17.96</td>
      <td>NaN</td>
      <td>18.00</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>100500</td>
      <td>20170928</td>
      <td>29442839.0</td>
      <td>1637650.0</td>
      <td>17.978713</td>
    </tr>
    <tr>
      <th>7</th>
      <td>17.99</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.00</td>
      <td>17.98</td>
      <td>NaN</td>
      <td>17.99</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>101000</td>
      <td>20170928</td>
      <td>8453291.0</td>
      <td>469911.0</td>
      <td>17.989132</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18.00</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.01</td>
      <td>17.99</td>
      <td>NaN</td>
      <td>18.00</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>101500</td>
      <td>20170928</td>
      <td>9820498.0</td>
      <td>545600.0</td>
      <td>17.999446</td>
    </tr>
    <tr>
      <th>9</th>
      <td>17.98</td>
      <td>600030</td>
      <td>20170928</td>
      <td>5M</td>
      <td>18.01</td>
      <td>17.95</td>
      <td>NaN</td>
      <td>18.00</td>
      <td>NaN</td>
      <td>600030.SH</td>
      <td>102000</td>
      <td>20170928</td>
      <td>30884646.0</td>
      <td>1719000.0</td>
      <td>17.966635</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>close</th>
      <th>code</th>
      <th>freq</th>
      <th>high</th>
      <th>low</th>
      <th>oi</th>
      <th>open</th>
      <th>presettle</th>
      <th>settle</th>
      <th>symbol</th>
      <th>trade_date</th>
      <th>trade_status</th>
      <th>turnover</th>
      <th>volume</th>
      <th>vwap</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>84.557890</td>
      <td>600832</td>
      <td>1d</td>
      <td>87.049772</td>
      <td>84.391764</td>
      <td>NaN</td>
      <td>86.883647</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121026</td>
      <td>交易</td>
      <td>27790568.0</td>
      <td>5381800.0</td>
      <td>85.78</td>
    </tr>
    <tr>
      <th>1</th>
      <td>84.724015</td>
      <td>600832</td>
      <td>1d</td>
      <td>85.554643</td>
      <td>84.391764</td>
      <td>NaN</td>
      <td>84.890141</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121029</td>
      <td>交易</td>
      <td>13203328.0</td>
      <td>2582557.0</td>
      <td>84.93</td>
    </tr>
    <tr>
      <th>2</th>
      <td>84.890141</td>
      <td>600832</td>
      <td>1d</td>
      <td>86.053019</td>
      <td>84.391764</td>
      <td>NaN</td>
      <td>85.056266</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121030</td>
      <td>交易</td>
      <td>16227051.0</td>
      <td>3170615.0</td>
      <td>85.02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>84.890141</td>
      <td>600832</td>
      <td>1d</td>
      <td>85.388517</td>
      <td>84.557890</td>
      <td>NaN</td>
      <td>85.056266</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121031</td>
      <td>交易</td>
      <td>10720069.0</td>
      <td>2097770.0</td>
      <td>84.89</td>
    </tr>
    <tr>
      <th>4</th>
      <td>86.053019</td>
      <td>600832</td>
      <td>1d</td>
      <td>86.385270</td>
      <td>85.056266</td>
      <td>NaN</td>
      <td>85.056266</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121101</td>
      <td>交易</td>
      <td>19721000.0</td>
      <td>3814712.0</td>
      <td>85.88</td>
    </tr>
    <tr>
      <th>5</th>
      <td>88.212651</td>
      <td>600832</td>
      <td>1d</td>
      <td>88.877153</td>
      <td>85.222392</td>
      <td>NaN</td>
      <td>86.385270</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121102</td>
      <td>交易</td>
      <td>57502794.0</td>
      <td>10927010.0</td>
      <td>87.42</td>
    </tr>
    <tr>
      <th>6</th>
      <td>87.880400</td>
      <td>600832</td>
      <td>1d</td>
      <td>89.541655</td>
      <td>87.215898</td>
      <td>NaN</td>
      <td>88.378777</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121105</td>
      <td>交易</td>
      <td>62725248.0</td>
      <td>11807741.0</td>
      <td>88.25</td>
    </tr>
    <tr>
      <th>7</th>
      <td>88.378777</td>
      <td>600832</td>
      <td>1d</td>
      <td>88.711028</td>
      <td>86.385270</td>
      <td>NaN</td>
      <td>87.714275</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121106</td>
      <td>交易</td>
      <td>55743439.0</td>
      <td>10595902.0</td>
      <td>87.40</td>
    </tr>
    <tr>
      <th>8</th>
      <td>88.046526</td>
      <td>600832</td>
      <td>1d</td>
      <td>88.544902</td>
      <td>87.548149</td>
      <td>NaN</td>
      <td>87.880400</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121107</td>
      <td>交易</td>
      <td>26376465.0</td>
      <td>4975333.0</td>
      <td>88.07</td>
    </tr>
    <tr>
      <th>9</th>
      <td>86.883647</td>
      <td>600832</td>
      <td>1d</td>
      <td>88.046526</td>
      <td>86.551396</td>
      <td>NaN</td>
      <td>87.382024</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>600832.SH</td>
      <td>20121108</td>
      <td>交易</td>
      <td>31516248.0</td>
      <td>6006363.0</td>
      <td>87.17</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>list_date</th>
      <th>market</th>
      <th>name</th>
      <th>status</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>19991110</td>
      <td>SH</td>
      <td>浦发银行</td>
      <td>1</td>
      <td>600000.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20001219</td>
      <td>SH</td>
      <td>民生银行</td>
      <td>1</td>
      <td>600016.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20030106</td>
      <td>SH</td>
      <td>中信证券</td>
      <td>1</td>
      <td>600030.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20021009</td>
      <td>SH</td>
      <td>中国联通</td>
      <td>1</td>
      <td>600050.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>19970807</td>
      <td>SH</td>
      <td>国金证券</td>
      <td>1</td>
      <td>600109.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20000526</td>
      <td>SH</td>
      <td>广汇能源</td>
      <td>1</td>
      <td>600256.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20010827</td>
      <td>SH</td>
      <td>贵州茅台</td>
      <td>1</td>
      <td>600519.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>19930316</td>
      <td>SH</td>
      <td>东方明珠</td>
      <td>1</td>
      <td>600637.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>19960312</td>
      <td>SH</td>
      <td>伊利股份</td>
      <td>1</td>
      <td>600887.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20091117</td>
      <td>SH</td>
      <td>招商证券</td>
      <td>1</td>
      <td>600999.SH</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>api</th>
      <th>comment</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>jz.instrumentInfo</td>
      <td>证券基本信息</td>
      <td>证券基础信息</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jz.secTradeCal</td>
      <td>交易日历</td>
      <td>交易日历</td>
    </tr>
    <tr>
      <th>2</th>
      <td>lb.indexCons</td>
      <td>指数成份股</td>
      <td>指数成份股</td>
    </tr>
    <tr>
      <th>3</th>
      <td>lb.indexInfo</td>
      <td>指数基本信息</td>
      <td>指数基本信息</td>
    </tr>
    <tr>
      <th>4</th>
      <td>lb.industryType</td>
      <td>行业代码表</td>
      <td>行业代码表</td>
    </tr>
    <tr>
      <th>5</th>
      <td>lb.mfNav</td>
      <td>公募基金净值</td>
      <td>公募基金净值</td>
    </tr>
    <tr>
      <th>6</th>
      <td>lb.secAdjFactor</td>
      <td>复权因子</td>
      <td>复权因子</td>
    </tr>
    <tr>
      <th>7</th>
      <td>lb.secDividend</td>
      <td>分红送股</td>
      <td>分红送股表</td>
    </tr>
    <tr>
      <th>8</th>
      <td>lb.secIndustry</td>
      <td>行业分类信息</td>
      <td>行业分类</td>
    </tr>
    <tr>
      <th>9</th>
      <td>lb.secSusp</td>
      <td>停复牌数据</td>
      <td>停复牌</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 查询jz.instrumentInfo接口的输入输出参数
df, msg = api.query(
    view="help.apiParam", 
    fields="", 
    filter="api=jz.instrumentInfo"
)
df.head(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>api</th>
      <th>comment</th>
      <th>dtype</th>
      <th>must</th>
      <th>param</th>
      <th>pname</th>
      <th>ptype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>inst_type</td>
      <td>证券类型</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>inst_type</td>
      <td>证券类型</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>status</td>
      <td>上市状态</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>symbol</td>
      <td>证券代码</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>Y</td>
      <td>symbol</td>
      <td>证券代码</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>5</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>Y</td>
      <td>name</td>
      <td>证券名称</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>6</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>Y</td>
      <td>list_date</td>
      <td>上市日期</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>7</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>delist_date</td>
      <td>退市日期</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>8</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>status</td>
      <td>上市状态</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>9</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>currency</td>
      <td>货币</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>10</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>buylot</td>
      <td>最小买入单位</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>11</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>selllot</td>
      <td>最大买入单位</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>12</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Double</td>
      <td>N</td>
      <td>pricetick</td>
      <td>最小变动单位</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>13</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>underlying</td>
      <td>对应标的</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>14</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>product</td>
      <td>合约品种</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>15</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>market</td>
      <td>交易所</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>market</td>
      <td>交易所</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>17</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>start_delistdate</td>
      <td>退市阶段(开始日期)</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>end_delistdate</td>
      <td>退市阶段(结束日期)</td>
      <td>IN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>Int</td>
      <td>N</td>
      <td>multiplier</td>
      <td>合约乘数</td>
      <td>OUT</td>
    </tr>
    <tr>
      <th>20</th>
      <td>jz.instrumentInfo</td>
      <td></td>
      <td>String</td>
      <td>N</td>
      <td>trade_date</td>
      <td>交易日</td>
      <td>IN</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>list_date</th>
      <th>name</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>19991110</td>
      <td>浦发银行</td>
      <td>600000.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20001219</td>
      <td>民生银行</td>
      <td>600016.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20030106</td>
      <td>中信证券</td>
      <td>600030.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20021009</td>
      <td>中国联通</td>
      <td>600050.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>19970807</td>
      <td>国金证券</td>
      <td>600109.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20000526</td>
      <td>广汇能源</td>
      <td>600256.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20010827</td>
      <td>贵州茅台</td>
      <td>600519.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>19930316</td>
      <td>东方明珠</td>
      <td>600637.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>19960312</td>
      <td>伊利股份</td>
      <td>600887.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20091117</td>
      <td>招商证券</td>
      <td>600999.SH</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 指数基本信息

df, msg = api.query(
    view="lb.indexInfo", 
    fields="", 
    filter=""
)
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>compname</th>
      <th>exchmarket</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>深圳证券交易所农林牧渔指数</td>
      <td>SZ</td>
      <td>399110.SZ</td>
    </tr>
    <tr>
      <th>1</th>
      <td>深圳证券交易所采掘业指数</td>
      <td>SZ</td>
      <td>399120.SZ</td>
    </tr>
    <tr>
      <th>2</th>
      <td>深圳证券交易所制造业指数</td>
      <td>SZ</td>
      <td>399130.SZ</td>
    </tr>
    <tr>
      <th>3</th>
      <td>深圳证券交易所食品饮料指数</td>
      <td>SZ</td>
      <td>399131.SZ</td>
    </tr>
    <tr>
      <th>4</th>
      <td>深圳证券交易所纺织服装指数</td>
      <td>SZ</td>
      <td>399132.SZ</td>
    </tr>
    <tr>
      <th>5</th>
      <td>深圳证券交易所木材家具指数</td>
      <td>SZ</td>
      <td>399133.SZ</td>
    </tr>
    <tr>
      <th>6</th>
      <td>深圳证券交易所造纸印刷指数</td>
      <td>SZ</td>
      <td>399134.SZ</td>
    </tr>
    <tr>
      <th>7</th>
      <td>深圳证券交易所石化塑胶指数</td>
      <td>SZ</td>
      <td>399135.SZ</td>
    </tr>
    <tr>
      <th>8</th>
      <td>深圳证券交易所电子指数</td>
      <td>SZ</td>
      <td>399136.SZ</td>
    </tr>
    <tr>
      <th>9</th>
      <td>深圳证券交易所金属非金属指数</td>
      <td>SZ</td>
      <td>399137.SZ</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 交易日历信息，只支持中国的交易日历

df, msg = api.query(
    view="jz.secTradeCal", 
    fields="", 
    filter=""
)
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>istradeday</th>
      <th>trade_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T</td>
      <td>19901219</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T</td>
      <td>19901220</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T</td>
      <td>19901221</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T</td>
      <td>19901224</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T</td>
      <td>19901225</td>
    </tr>
    <tr>
      <th>5</th>
      <td>T</td>
      <td>19901226</td>
    </tr>
    <tr>
      <th>6</th>
      <td>T</td>
      <td>19901227</td>
    </tr>
    <tr>
      <th>7</th>
      <td>T</td>
      <td>19901228</td>
    </tr>
    <tr>
      <th>8</th>
      <td>T</td>
      <td>19901231</td>
    </tr>
    <tr>
      <th>9</th>
      <td>T</td>
      <td>19910102</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 行业代码表

df, msg = api.query(
    view="lb.industryType", 
    fields="", 
    filter="industry_src=SW&level=1"
)
df.head(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>industry1_code</th>
      <th>industry2_code</th>
      <th>industry3_code</th>
      <th>industry_name</th>
      <th>industry_src</th>
      <th>level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>110000</td>
      <td></td>
      <td></td>
      <td>农林牧渔</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>210000</td>
      <td></td>
      <td></td>
      <td>采掘</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>220000</td>
      <td></td>
      <td></td>
      <td>化工</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>230000</td>
      <td></td>
      <td></td>
      <td>钢铁</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>240000</td>
      <td></td>
      <td></td>
      <td>有色金属</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>270000</td>
      <td></td>
      <td></td>
      <td>电子</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>280000</td>
      <td></td>
      <td></td>
      <td>汽车</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>330000</td>
      <td></td>
      <td></td>
      <td>家用电器</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>340000</td>
      <td></td>
      <td></td>
      <td>食品饮料</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>350000</td>
      <td></td>
      <td></td>
      <td>纺织服装</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>360000</td>
      <td></td>
      <td></td>
      <td>轻工制造</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>370000</td>
      <td></td>
      <td></td>
      <td>医药生物</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>410000</td>
      <td></td>
      <td></td>
      <td>公用事业</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>420000</td>
      <td></td>
      <td></td>
      <td>交通运输</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>430000</td>
      <td></td>
      <td></td>
      <td>房地产</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>450000</td>
      <td></td>
      <td></td>
      <td>商业贸易</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>460000</td>
      <td></td>
      <td></td>
      <td>休闲服务</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>480000</td>
      <td></td>
      <td></td>
      <td>银行</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>490000</td>
      <td></td>
      <td></td>
      <td>非银金融</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>510000</td>
      <td></td>
      <td></td>
      <td>综合</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>610000</td>
      <td></td>
      <td></td>
      <td>建筑材料</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>620000</td>
      <td></td>
      <td></td>
      <td>建筑装饰</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>630000</td>
      <td></td>
      <td></td>
      <td>电气设备</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>640000</td>
      <td></td>
      <td></td>
      <td>机械设备</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>650000</td>
      <td></td>
      <td></td>
      <td>国防军工</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>710000</td>
      <td></td>
      <td></td>
      <td>计算机</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>26</th>
      <td>720000</td>
      <td></td>
      <td></td>
      <td>传媒</td>
      <td>sw</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>730000</td>
      <td></td>
      <td></td>
      <td>通信</td>
      <td>sw</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ann_date</th>
      <th>bonus_list_date</th>
      <th>cash</th>
      <th>cash_tax</th>
      <th>cashpay_date</th>
      <th>div_enddate</th>
      <th>exdiv_date</th>
      <th>publish_date</th>
      <th>record_date</th>
      <th>share_ratio</th>
      <th>share_trans_ratio</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20020604</td>
      <td></td>
      <td>0.166</td>
      <td>0.0000</td>
      <td>20020604</td>
      <td>20011231</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20030418</td>
      <td></td>
      <td>0.120</td>
      <td>0.0960</td>
      <td>20030723</td>
      <td>20021231</td>
      <td>20030716</td>
      <td>20030708</td>
      <td>20030715</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20040218</td>
      <td>20040512</td>
      <td>0.092</td>
      <td>0.0740</td>
      <td>20040517</td>
      <td>20031231</td>
      <td>20040511</td>
      <td>20040428</td>
      <td>20040510</td>
      <td>0.0</td>
      <td>0.20000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20050331</td>
      <td>20050621</td>
      <td>0.110</td>
      <td>0.0990</td>
      <td>20050624</td>
      <td>20041231</td>
      <td>20050620</td>
      <td>20050614</td>
      <td>20050617</td>
      <td>0.0</td>
      <td>0.50000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20060412</td>
      <td></td>
      <td>0.080</td>
      <td>0.0720</td>
      <td>20060621</td>
      <td>20051231</td>
      <td>20060616</td>
      <td>20060612</td>
      <td>20060615</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20051230</td>
      <td>20060227</td>
      <td>0.000</td>
      <td>0.0000</td>
      <td></td>
      <td>20060223</td>
      <td>20060224</td>
      <td>20060222</td>
      <td>20060223</td>
      <td>0.0</td>
      <td>0.08589</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20060720</td>
      <td></td>
      <td>0.180</td>
      <td>0.1620</td>
      <td>20060927</td>
      <td>20060719</td>
      <td>20060921</td>
      <td>20060915</td>
      <td>20060920</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20070417</td>
      <td></td>
      <td>0.120</td>
      <td>0.1080</td>
      <td>20070710</td>
      <td>20061231</td>
      <td>20070704</td>
      <td>20070628</td>
      <td>20070703</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20080319</td>
      <td></td>
      <td>0.280</td>
      <td>0.2520</td>
      <td>20080801</td>
      <td>20071231</td>
      <td>20080728</td>
      <td>20080722</td>
      <td>20080725</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20090425</td>
      <td>20090706</td>
      <td>0.100</td>
      <td>0.0600</td>
      <td>20090709</td>
      <td>20081231</td>
      <td>20090703</td>
      <td>20090629</td>
      <td>20090702</td>
      <td>0.3</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20100414</td>
      <td></td>
      <td>0.210</td>
      <td>0.1890</td>
      <td>20100708</td>
      <td>20091231</td>
      <td>20100701</td>
      <td>20100625</td>
      <td>20100630</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20110401</td>
      <td></td>
      <td>0.290</td>
      <td>0.2610</td>
      <td>20110616</td>
      <td>20101231</td>
      <td>20110610</td>
      <td>20110603</td>
      <td>20110609</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20120329</td>
      <td></td>
      <td>0.420</td>
      <td>0.3780</td>
      <td>20120613</td>
      <td>20111231</td>
      <td>20120607</td>
      <td>20120601</td>
      <td>20120606</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20130329</td>
      <td></td>
      <td>0.630</td>
      <td>0.5985</td>
      <td>20130619</td>
      <td>20121231</td>
      <td>20130613</td>
      <td>20130604</td>
      <td>20130607</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20140329</td>
      <td></td>
      <td>0.620</td>
      <td>0.5890</td>
      <td>20140711</td>
      <td>20131231</td>
      <td>20140711</td>
      <td>20140703</td>
      <td>20140710</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20150319</td>
      <td></td>
      <td>0.670</td>
      <td>0.6365</td>
      <td>20150703</td>
      <td>20141231</td>
      <td>20150703</td>
      <td>20150625</td>
      <td>20150702</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20160331</td>
      <td></td>
      <td>0.690</td>
      <td>0.6900</td>
      <td>20160713</td>
      <td>20151231</td>
      <td>20160713</td>
      <td>20160705</td>
      <td>20160712</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20170325</td>
      <td></td>
      <td>0.740</td>
      <td>0.7400</td>
      <td>20170614</td>
      <td>20161231</td>
      <td>20170614</td>
      <td>20170606</td>
      <td>20170613</td>
      <td>0.0</td>
      <td>0.00000</td>
      <td>600036.SH</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 股票停复牌数据

df, msg = api.query(
    view="lb.secSusp", 
    fields="", 
    filter="symbol=600036.SH"
)
df.head(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ann_date</th>
      <th>resu_date</th>
      <th>susp_date</th>
      <th>susp_reason</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20080602</td>
      <td>20080603</td>
      <td>20080602</td>
      <td>重要事项未公告</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20080603</td>
      <td>20080603</td>
      <td>20080603</td>
      <td>刊登重要公告</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20080627</td>
      <td>20080630</td>
      <td>20080627</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20090227</td>
      <td>20090302</td>
      <td>20090227</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20090619</td>
      <td>20090622</td>
      <td>20090619</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20091019</td>
      <td>20091020</td>
      <td>20091019</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20100623</td>
      <td>20100624</td>
      <td>20100623</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20110530</td>
      <td>20110531</td>
      <td>20110530</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20110909</td>
      <td>20110913</td>
      <td>20110909</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20120530</td>
      <td>20120531</td>
      <td>20120530</td>
      <td>召开股东大会</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20130904</td>
      <td>20130905</td>
      <td>20130828</td>
      <td>刊登重要公告</td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20150410</td>
      <td>20150413</td>
      <td>20150403</td>
      <td>刊登重要公告</td>
      <td>600036.SH</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 股票复权因子数据

df, msg = api.query(
    view="lb.secAdjFactor", 
    fields="", 
    filter="symbol=600036.SH"
)
df.tail(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adjust_factor</th>
      <th>symbol</th>
      <th>trade_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3756</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170921</td>
    </tr>
    <tr>
      <th>3757</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170922</td>
    </tr>
    <tr>
      <th>3758</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170925</td>
    </tr>
    <tr>
      <th>3759</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170926</td>
    </tr>
    <tr>
      <th>3760</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170927</td>
    </tr>
    <tr>
      <th>3761</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170928</td>
    </tr>
    <tr>
      <th>3762</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20170929</td>
    </tr>
    <tr>
      <th>3763</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171009</td>
    </tr>
    <tr>
      <th>3764</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171010</td>
    </tr>
    <tr>
      <th>3765</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171011</td>
    </tr>
    <tr>
      <th>3766</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171012</td>
    </tr>
    <tr>
      <th>3767</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171013</td>
    </tr>
    <tr>
      <th>3768</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171016</td>
    </tr>
    <tr>
      <th>3769</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171017</td>
    </tr>
    <tr>
      <th>3770</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171018</td>
    </tr>
    <tr>
      <th>3771</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171019</td>
    </tr>
    <tr>
      <th>3772</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171020</td>
    </tr>
    <tr>
      <th>3773</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171023</td>
    </tr>
    <tr>
      <th>3774</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171024</td>
    </tr>
    <tr>
      <th>3775</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171025</td>
    </tr>
    <tr>
      <th>3776</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171026</td>
    </tr>
    <tr>
      <th>3777</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171027</td>
    </tr>
    <tr>
      <th>3778</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171030</td>
    </tr>
    <tr>
      <th>3779</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171031</td>
    </tr>
    <tr>
      <th>3780</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171101</td>
    </tr>
    <tr>
      <th>3781</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171102</td>
    </tr>
    <tr>
      <th>3782</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171103</td>
    </tr>
    <tr>
      <th>3783</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171106</td>
    </tr>
    <tr>
      <th>3784</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171107</td>
    </tr>
    <tr>
      <th>3785</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20171108</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3826</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180105</td>
    </tr>
    <tr>
      <th>3827</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180108</td>
    </tr>
    <tr>
      <th>3828</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180109</td>
    </tr>
    <tr>
      <th>3829</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180110</td>
    </tr>
    <tr>
      <th>3830</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180111</td>
    </tr>
    <tr>
      <th>3831</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180112</td>
    </tr>
    <tr>
      <th>3832</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180115</td>
    </tr>
    <tr>
      <th>3833</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180116</td>
    </tr>
    <tr>
      <th>3834</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180117</td>
    </tr>
    <tr>
      <th>3835</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180118</td>
    </tr>
    <tr>
      <th>3836</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180119</td>
    </tr>
    <tr>
      <th>3837</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180122</td>
    </tr>
    <tr>
      <th>3838</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180123</td>
    </tr>
    <tr>
      <th>3839</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180124</td>
    </tr>
    <tr>
      <th>3840</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180125</td>
    </tr>
    <tr>
      <th>3841</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180126</td>
    </tr>
    <tr>
      <th>3842</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180129</td>
    </tr>
    <tr>
      <th>3843</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180130</td>
    </tr>
    <tr>
      <th>3844</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180131</td>
    </tr>
    <tr>
      <th>3845</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180201</td>
    </tr>
    <tr>
      <th>3846</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180202</td>
    </tr>
    <tr>
      <th>3847</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180205</td>
    </tr>
    <tr>
      <th>3848</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180206</td>
    </tr>
    <tr>
      <th>3849</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180207</td>
    </tr>
    <tr>
      <th>3850</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180208</td>
    </tr>
    <tr>
      <th>3851</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180209</td>
    </tr>
    <tr>
      <th>3852</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180212</td>
    </tr>
    <tr>
      <th>3853</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180213</td>
    </tr>
    <tr>
      <th>3854</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180214</td>
    </tr>
    <tr>
      <th>3855</th>
      <td>4.62913</td>
      <td>600036.SH</td>
      <td>20180222</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 3 columns</p>
</div>




```python
# 股票行业分类数据

df, msg = api.query(
    view="lb.secIndustry", 
    fields="", 
    filter="symbol=600030.SH,600031.SH&industry_src=SW"
)
df.tail(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>in_date</th>
      <th>industry1_code</th>
      <th>industry1_name</th>
      <th>industry2_code</th>
      <th>industry2_name</th>
      <th>industry3_code</th>
      <th>industry3_name</th>
      <th>industry4_code</th>
      <th>industry4_name</th>
      <th>industry_src</th>
      <th>out_date</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20140101</td>
      <td>490000</td>
      <td>非银金融</td>
      <td>490100</td>
      <td>证券</td>
      <td>490101</td>
      <td>证券</td>
      <td>490101</td>
      <td>证券</td>
      <td>sw</td>
      <td></td>
      <td>600030.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20140101</td>
      <td>640000</td>
      <td>机械设备</td>
      <td>640200</td>
      <td>专用设备</td>
      <td>640201</td>
      <td>工程机械</td>
      <td>640201</td>
      <td>工程机械</td>
      <td>sw</td>
      <td></td>
      <td>600031.SH</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 指数成份股数据

df, msg = api.query(
    view="lb.indexCons", 
    fields="", 
    filter="index_code=000016.SH&start_date=20170101&end_date=20171229"
)
df.tail(100)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>in_date</th>
      <th>index_code</th>
      <th>out_date</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600000.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600016.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>600019.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600028.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20160613</td>
      <td>000016.SH</td>
      <td></td>
      <td>600029.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600030.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600050.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td>20171208</td>
      <td>600100.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600104.SH</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20141215</td>
      <td>000016.SH</td>
      <td>20170609</td>
      <td>600109.SH</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20110104</td>
      <td>000016.SH</td>
      <td></td>
      <td>600111.SH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>600309.SH</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600340.SH</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td>20171208</td>
      <td>600485.SH</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20130701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600518.SH</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20050701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600519.SH</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td></td>
      <td>600547.SH</td>
    </tr>
    <tr>
      <th>18</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600606.SH</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20131216</td>
      <td>000016.SH</td>
      <td>20170609</td>
      <td>600637.SH</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20090105</td>
      <td>000016.SH</td>
      <td></td>
      <td>600837.SH</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20120702</td>
      <td>000016.SH</td>
      <td></td>
      <td>600887.SH</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20150521</td>
      <td>000016.SH</td>
      <td>20170609</td>
      <td>600893.SH</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601988.SH</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20070104</td>
      <td>000016.SH</td>
      <td></td>
      <td>600048.SH</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20060815</td>
      <td>000016.SH</td>
      <td></td>
      <td>601006.SH</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20061110</td>
      <td>000016.SH</td>
      <td></td>
      <td>601398.SH</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20070123</td>
      <td>000016.SH</td>
      <td></td>
      <td>601628.SH</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20070226</td>
      <td>000016.SH</td>
      <td></td>
      <td>601166.SH</td>
    </tr>
    <tr>
      <th>29</th>
      <td>20070315</td>
      <td>000016.SH</td>
      <td></td>
      <td>601318.SH</td>
    </tr>
    <tr>
      <th>30</th>
      <td>20141215</td>
      <td>000016.SH</td>
      <td>20170609</td>
      <td>601998.SH</td>
    </tr>
    <tr>
      <th>31</th>
      <td>20070529</td>
      <td>000016.SH</td>
      <td></td>
      <td>601328.SH</td>
    </tr>
    <tr>
      <th>32</th>
      <td>20090105</td>
      <td>000016.SH</td>
      <td></td>
      <td>601169.SH</td>
    </tr>
    <tr>
      <th>33</th>
      <td>20071023</td>
      <td>000016.SH</td>
      <td></td>
      <td>601088.SH</td>
    </tr>
    <tr>
      <th>34</th>
      <td>20071119</td>
      <td>000016.SH</td>
      <td></td>
      <td>601857.SH</td>
    </tr>
    <tr>
      <th>35</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601390.SH</td>
    </tr>
    <tr>
      <th>36</th>
      <td>20080701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601601.SH</td>
    </tr>
    <tr>
      <th>37</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601186.SH</td>
    </tr>
    <tr>
      <th>38</th>
      <td>20100104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601668.SH</td>
    </tr>
    <tr>
      <th>39</th>
      <td>20110701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601766.SH</td>
    </tr>
    <tr>
      <th>40</th>
      <td>20160613</td>
      <td>000016.SH</td>
      <td>20171208</td>
      <td>601788.SH</td>
    </tr>
    <tr>
      <th>41</th>
      <td>20130701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600999.SH</td>
    </tr>
    <tr>
      <th>42</th>
      <td>20110701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601989.SH</td>
    </tr>
    <tr>
      <th>43</th>
      <td>20130104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601688.SH</td>
    </tr>
    <tr>
      <th>44</th>
      <td>20100729</td>
      <td>000016.SH</td>
      <td></td>
      <td>601288.SH</td>
    </tr>
    <tr>
      <th>45</th>
      <td>20160613</td>
      <td>000016.SH</td>
      <td>20170609</td>
      <td>601377.SH</td>
    </tr>
    <tr>
      <th>46</th>
      <td>20110104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601818.SH</td>
    </tr>
    <tr>
      <th>47</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td>20171208</td>
      <td>601901.SH</td>
    </tr>
    <tr>
      <th>48</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>601669.SH</td>
    </tr>
    <tr>
      <th>49</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601800.SH</td>
    </tr>
    <tr>
      <th>50</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601336.SH</td>
    </tr>
    <tr>
      <th>51</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>603993.SH</td>
    </tr>
    <tr>
      <th>52</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601211.SH</td>
    </tr>
    <tr>
      <th>53</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>600958.SH</td>
    </tr>
    <tr>
      <th>54</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td>20171208</td>
      <td>601198.SH</td>
    </tr>
    <tr>
      <th>55</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601985.SH</td>
    </tr>
    <tr>
      <th>56</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>601878.SH</td>
    </tr>
    <tr>
      <th>57</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>601229.SH</td>
    </tr>
    <tr>
      <th>58</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600919.SH</td>
    </tr>
    <tr>
      <th>59</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>601881.SH</td>
    </tr>
  </tbody>
</table>
</div>



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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>in_date</th>
      <th>index_code</th>
      <th>out_date</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600000.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600016.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>600019.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600028.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20160613</td>
      <td>000016.SH</td>
      <td></td>
      <td>600029.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600030.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600036.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600050.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20040102</td>
      <td>000016.SH</td>
      <td></td>
      <td>600104.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20110104</td>
      <td>000016.SH</td>
      <td></td>
      <td>600111.SH</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>600309.SH</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600340.SH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20130701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600518.SH</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20050701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600519.SH</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20161212</td>
      <td>000016.SH</td>
      <td></td>
      <td>600547.SH</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600606.SH</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20090105</td>
      <td>000016.SH</td>
      <td></td>
      <td>600837.SH</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20120702</td>
      <td>000016.SH</td>
      <td></td>
      <td>600887.SH</td>
    </tr>
    <tr>
      <th>18</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601988.SH</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20070104</td>
      <td>000016.SH</td>
      <td></td>
      <td>600048.SH</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20060815</td>
      <td>000016.SH</td>
      <td></td>
      <td>601006.SH</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20061110</td>
      <td>000016.SH</td>
      <td></td>
      <td>601398.SH</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20070123</td>
      <td>000016.SH</td>
      <td></td>
      <td>601628.SH</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20070226</td>
      <td>000016.SH</td>
      <td></td>
      <td>601166.SH</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20070315</td>
      <td>000016.SH</td>
      <td></td>
      <td>601318.SH</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20070529</td>
      <td>000016.SH</td>
      <td></td>
      <td>601328.SH</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20090105</td>
      <td>000016.SH</td>
      <td></td>
      <td>601169.SH</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20071023</td>
      <td>000016.SH</td>
      <td></td>
      <td>601088.SH</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20071119</td>
      <td>000016.SH</td>
      <td></td>
      <td>601857.SH</td>
    </tr>
    <tr>
      <th>29</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601390.SH</td>
    </tr>
    <tr>
      <th>30</th>
      <td>20080701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601601.SH</td>
    </tr>
    <tr>
      <th>31</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601186.SH</td>
    </tr>
    <tr>
      <th>32</th>
      <td>20100104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601668.SH</td>
    </tr>
    <tr>
      <th>33</th>
      <td>20110701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601766.SH</td>
    </tr>
    <tr>
      <th>34</th>
      <td>20130701</td>
      <td>000016.SH</td>
      <td></td>
      <td>600999.SH</td>
    </tr>
    <tr>
      <th>35</th>
      <td>20110701</td>
      <td>000016.SH</td>
      <td></td>
      <td>601989.SH</td>
    </tr>
    <tr>
      <th>36</th>
      <td>20130104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601688.SH</td>
    </tr>
    <tr>
      <th>37</th>
      <td>20100729</td>
      <td>000016.SH</td>
      <td></td>
      <td>601288.SH</td>
    </tr>
    <tr>
      <th>38</th>
      <td>20110104</td>
      <td>000016.SH</td>
      <td></td>
      <td>601818.SH</td>
    </tr>
    <tr>
      <th>39</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>601669.SH</td>
    </tr>
    <tr>
      <th>40</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>601800.SH</td>
    </tr>
    <tr>
      <th>41</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601336.SH</td>
    </tr>
    <tr>
      <th>42</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>603993.SH</td>
    </tr>
    <tr>
      <th>43</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601211.SH</td>
    </tr>
    <tr>
      <th>44</th>
      <td>20150615</td>
      <td>000016.SH</td>
      <td></td>
      <td>600958.SH</td>
    </tr>
    <tr>
      <th>45</th>
      <td>20151214</td>
      <td>000016.SH</td>
      <td></td>
      <td>601985.SH</td>
    </tr>
    <tr>
      <th>46</th>
      <td>20171211</td>
      <td>000016.SH</td>
      <td></td>
      <td>601878.SH</td>
    </tr>
    <tr>
      <th>47</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>601229.SH</td>
    </tr>
    <tr>
      <th>48</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>600919.SH</td>
    </tr>
    <tr>
      <th>49</th>
      <td>20170612</td>
      <td>000016.SH</td>
      <td></td>
      <td>601881.SH</td>
    </tr>
  </tbody>
</table>
</div>




```python
# 公募基金净值

df, msg = api.query(
    view="lb.mfNav", 
    fields="", 
    filter="symbol=510050.SH&start_pdate=20170101&end_pdate=20180101"
)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ann_date</th>
      <th>nav</th>
      <th>nav_accumulated</th>
      <th>price_date</th>
      <th>symbol</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20170104</td>
      <td>2.310</td>
      <td>3.142</td>
      <td>20170103</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20170105</td>
      <td>2.324</td>
      <td>3.158</td>
      <td>20170104</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20170106</td>
      <td>2.325</td>
      <td>3.160</td>
      <td>20170105</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20170107</td>
      <td>2.312</td>
      <td>3.144</td>
      <td>20170106</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20170110</td>
      <td>2.321</td>
      <td>3.155</td>
      <td>20170109</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20170111</td>
      <td>2.315</td>
      <td>3.148</td>
      <td>20170110</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20170112</td>
      <td>2.303</td>
      <td>3.134</td>
      <td>20170111</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20170113</td>
      <td>2.298</td>
      <td>3.128</td>
      <td>20170112</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20170114</td>
      <td>2.311</td>
      <td>3.143</td>
      <td>20170113</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20170117</td>
      <td>2.340</td>
      <td>3.177</td>
      <td>20170116</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20170118</td>
      <td>2.332</td>
      <td>3.168</td>
      <td>20170117</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>11</th>
      <td>20170119</td>
      <td>2.345</td>
      <td>3.183</td>
      <td>20170118</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>20170120</td>
      <td>2.337</td>
      <td>3.174</td>
      <td>20170119</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>13</th>
      <td>20170121</td>
      <td>2.349</td>
      <td>3.188</td>
      <td>20170120</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>14</th>
      <td>20170124</td>
      <td>2.349</td>
      <td>3.188</td>
      <td>20170123</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>15</th>
      <td>20170125</td>
      <td>2.354</td>
      <td>3.194</td>
      <td>20170124</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20170126</td>
      <td>2.360</td>
      <td>3.201</td>
      <td>20170125</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>17</th>
      <td>20170127</td>
      <td>2.365</td>
      <td>3.207</td>
      <td>20170126</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>18</th>
      <td>20170204</td>
      <td>2.341</td>
      <td>3.179</td>
      <td>20170203</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20170207</td>
      <td>2.345</td>
      <td>3.183</td>
      <td>20170206</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20170208</td>
      <td>2.339</td>
      <td>3.176</td>
      <td>20170207</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20170209</td>
      <td>2.347</td>
      <td>3.186</td>
      <td>20170208</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>22</th>
      <td>20170210</td>
      <td>2.355</td>
      <td>3.195</td>
      <td>20170209</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20170211</td>
      <td>2.368</td>
      <td>3.211</td>
      <td>20170210</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>24</th>
      <td>20170214</td>
      <td>2.379</td>
      <td>3.224</td>
      <td>20170213</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>25</th>
      <td>20170215</td>
      <td>2.373</td>
      <td>3.216</td>
      <td>20170214</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>26</th>
      <td>20170216</td>
      <td>2.372</td>
      <td>3.215</td>
      <td>20170215</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20170217</td>
      <td>2.377</td>
      <td>3.221</td>
      <td>20170216</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>28</th>
      <td>20170218</td>
      <td>2.363</td>
      <td>3.205</td>
      <td>20170217</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>29</th>
      <td>20170221</td>
      <td>2.393</td>
      <td>3.240</td>
      <td>20170220</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>216</th>
      <td>20171122</td>
      <td>3.045</td>
      <td>4.012</td>
      <td>20171121</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>217</th>
      <td>20171123</td>
      <td>3.070</td>
      <td>4.042</td>
      <td>20171122</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>218</th>
      <td>20171124</td>
      <td>2.997</td>
      <td>3.955</td>
      <td>20171123</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>219</th>
      <td>20171125</td>
      <td>2.993</td>
      <td>3.950</td>
      <td>20171124</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>220</th>
      <td>20171128</td>
      <td>2.973</td>
      <td>3.927</td>
      <td>20171127</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>221</th>
      <td>20171129</td>
      <td>2.899</td>
      <td>3.903</td>
      <td>20171128</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>222</th>
      <td>20171130</td>
      <td>2.894</td>
      <td>3.897</td>
      <td>20171129</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>223</th>
      <td>20171201</td>
      <td>2.865</td>
      <td>3.863</td>
      <td>20171130</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>224</th>
      <td>20171202</td>
      <td>2.843</td>
      <td>3.837</td>
      <td>20171201</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>225</th>
      <td>20171205</td>
      <td>2.862</td>
      <td>3.859</td>
      <td>20171204</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>226</th>
      <td>20171206</td>
      <td>2.911</td>
      <td>3.917</td>
      <td>20171205</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>227</th>
      <td>20171207</td>
      <td>2.875</td>
      <td>3.875</td>
      <td>20171206</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>228</th>
      <td>20171208</td>
      <td>2.848</td>
      <td>3.843</td>
      <td>20171207</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>229</th>
      <td>20171209</td>
      <td>2.866</td>
      <td>3.864</td>
      <td>20171208</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>230</th>
      <td>20171212</td>
      <td>2.899</td>
      <td>3.903</td>
      <td>20171211</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>231</th>
      <td>20171213</td>
      <td>2.850</td>
      <td>3.845</td>
      <td>20171212</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>232</th>
      <td>20171214</td>
      <td>2.872</td>
      <td>3.871</td>
      <td>20171213</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>233</th>
      <td>20171215</td>
      <td>2.849</td>
      <td>3.844</td>
      <td>20171214</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>234</th>
      <td>20171216</td>
      <td>2.820</td>
      <td>3.810</td>
      <td>20171215</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>235</th>
      <td>20171219</td>
      <td>2.828</td>
      <td>3.819</td>
      <td>20171218</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>236</th>
      <td>20171220</td>
      <td>2.872</td>
      <td>3.871</td>
      <td>20171219</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>237</th>
      <td>20171221</td>
      <td>2.879</td>
      <td>3.879</td>
      <td>20171220</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>238</th>
      <td>20171222</td>
      <td>2.894</td>
      <td>3.897</td>
      <td>20171221</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>239</th>
      <td>20171223</td>
      <td>2.880</td>
      <td>3.881</td>
      <td>20171222</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>240</th>
      <td>20171226</td>
      <td>2.879</td>
      <td>3.879</td>
      <td>20171225</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>241</th>
      <td>20171227</td>
      <td>2.893</td>
      <td>3.896</td>
      <td>20171226</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>242</th>
      <td>20171228</td>
      <td>2.838</td>
      <td>3.831</td>
      <td>20171227</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>243</th>
      <td>20171229</td>
      <td>2.858</td>
      <td>3.855</td>
      <td>20171228</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>244</th>
      <td>20171230</td>
      <td>2.859</td>
      <td>3.856</td>
      <td>20171229</td>
      <td>510050.SH</td>
    </tr>
    <tr>
      <th>245</th>
      <td>20180101</td>
      <td>2.859</td>
      <td>3.856</td>
      <td>20171231</td>
      <td>510050.SH</td>
    </tr>
  </tbody>
</table>
<p>246 rows × 5 columns</p>
</div>


