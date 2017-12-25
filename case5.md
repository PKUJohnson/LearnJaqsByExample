# case 5：了解行情系统

股票行情是大家都熟知的概念，但你真的了解行情吗？如何才能构建一个自己的行情系统？

本文将为你详细解释行情系统的业务和技术细节。

## 一个证券交易是如何完成的

证券包括股票、期货、期权、ETF等交易品种，其买卖交易的原理基本相同。下图以股票为例，描述一个交易是如何完成的。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case5-1.png)

在本例中：
+ 投资者A发送一个买入委托，标的为600036.SH（招商银行），价格为29.55，数量为1000股。
+ 投资者B发送一个卖出委托，标的为600036.SH（招商银行），价格为29.55，数量为1000股。
+ 两个委托经过经纪商，最终被发送到上海证券交易所，上交所对两笔交易进行撮合，形成一笔成交。
+ 日终，中国登记结算公司会对上述交易进行结算，并将股票从投资者A过户到投资者B，将资金从投资者B过户到投资者A。
+ 券商将在扣除相应的交易费用后，更新相应的投资者账户资金信息。
+ 撮合成交后，市场成交量会增加1000，成交金额会增加29550。

这里面只是一个简单的例子，实际的交易撮合机制比较复杂，涉及订单优先原则、撮合价格机制、订单簿、订单类型等，在以后的文章中再做详细介绍。

## 什么是市场行情

由于有交易产生，市场的买卖信息会不断的发生变化，揭示最新市场的信息，就是所谓的行情。这是通达信行情软件的截图：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case5-2.png)

行情信息主要包括：

(1) 最新成交时间、总成交量、总成绩金额
(2) 今日开盘价、最高价、最低价、最新价
(3) 涨停价、跌停价
(4) 买卖队列信息
(5) 持仓量、结算价(适用期货和期权合约) 

在JAQS里，可以通过下面的代码，快速获取行情信息：

```python
from jaqs.data import DataApi
api = DataApi(addr='tcp://data.tushare.org:8910')
api.login("phone", "token") 

df,msg = api.quote("600036.SH", fields="open,high,low,last,volume")

```

返回的行情信息（即fields字段的范围）如下：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| symbol | string | 标的代码 |
| code | string | 交易所原始代码 |
| date | int | 自然日,YYYYMMDD格式，如20170823 |
| time | int | 时间，精确到毫秒，如14:21:05.330记为142105330 |
| trade\_date | int | YYYYMMDD格式，如20170823 |
| open | double | 开盘价 |
| high | double | 最高价 |
| low | double | 最低价 |
| last | double | 最新价 |
| close | double | 收盘价 |
| volume | double | 成交量（总） |
| turnover | double | 成交金额（总） |
| vwap | double | 截止到行情时间的日内成交均价 |
| oi | double | 持仓总量 |
| settle | double | 今结算价 |
| iopv | double | 净值估值 |
| limit\_up | double | 涨停价 |
| limit\_down | double | 跌停价 |
| preclose | double | 昨收盘价 |
| presettle | double | 昨结算价 |
| preoi | double | 昨持仓 |
| askprice1 | double | 申卖价1 |
| askprice2 | double | 申卖价2 |
| askprice3 | double | 申卖价3 |
| askprice4 | double | 申卖价4 |
| askprice5 | double | 申卖价5 |
| bidprice1 | double | 申买价1 |
| bidprice2 | double | 申买价2 |
| bidprice3 | double | 申买价3 |
| bidprice4 | double | 申买价4 |
| bidprice5 | double | 申买价5 |
| askvolume1 | double | 申卖量1 |
| askvolume2 | double | 申卖量2 |
| askvolume3 | double | 申卖量3 |
| askvolume4 | double | 申卖量4 |
| askvolume5 | double | 申卖量5 |
| bidvolume1 | double | 申买量1 |
| bidvolume2 | double | 申买量2 |
| bidvolume3 | double | 申买量3 |
| bidvolume4 | double | 申买量4 |
| bidvolume5 | double | 申买量5 |

## 市场行情的发送频率

交易所的交易信息是在不断更新的，交易所一般会按照某个固定的频率对市场进行快照，然后通过行情系统发送给出来，一般称为tick。

+ 沪深股票交易所Level1行情的频率是每3秒一次，提供5档委托队列信息
+ 期货Level1行情是每0.5秒一次，提供1档委托队列信息

+ 沪深股票交易所Level2行情的频率是每3秒一次，提供10档委托队列信息
+ 期货Level2行情是每0.25秒一次，提供5档委托队列信息

可见，level2的行情刷新速度比level1快，而且提供的委托队列信息更多。

## 什么是K线

tick数据由于是瞬时切片信息，数据量大且容易跳动，因此人们发明了一种称为K线的行情聚合方法，
即将一段时间内接收到的所有tick聚合成一个K线的点，包含open,high,low,last,volume,turnover,oi等信息。

```
open = 时段内第一个tick成交价
last = 时段内最后一个tick成交价
high = 时段内所有tick最高成交价
low  = 时段内所有tick最低成交价
volume   = 时段内成交数量
turnover = 时段内成交金额
oi   = 时段内最后一个tick的持仓量
```

根据时间范围不同，K线通常有1分钟、5分钟、15分钟、日等几种形式。

如果是以日为单位，一般也称为日线。

由于K线是一段时间的统计，会平抑瞬间的抖动，统计规律更加稳定，常用于各类量化研究模型。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case5-3.png)

上图是600036.SH的1分钟线数据，选取的点是13点49分的样本点。

在JAQS里，可以通过下面的代码，快速获取K线信息：

```python
from jaqs.data import DataApi
api = DataApi(addr='tcp://data.tushare.org:8910')
api.login("phone", "token") 

df,msg = api.bar(
            symbol="600030.SH", 
            trade_date=20170928, 
            freq="1M",
            start_time= 90000,
            end_time= 160000,
            fields="open,high,low,last,volume")
```
freq参数可以1M、5M、15M，trade_date=0表示取当日K线信息。

如果是日线，可以用下面的代码获取：

```python
df, msg = api.daily(
                symbol="600036.SH", 
                start_date=20121026,
                end_date=20121130, 
                fields="", 
                adjust_mode="post")
```

## 什么是股票复权

股票由于会有分红或者拆股的操作，会导致股票的价格在次日发生跳变，如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case5-4.png)

603888.SH（新华网）在2017年6月21日进行了分红，方案是10送15，因此次日股价直接从84.89跳变成33.96（84.89/2.5）

股票价格跳动会使得基于价格的研究，数值计算变得复杂，因此发明了复权因子，可根据复权因子计算出复权价格。

在复权后的价格上可以直接进行数值计算，例如计算MA5或者MA10。

复权有两种计算方法：

+ 前复权，即以历史某天的价格为基础，根据复权因子调整后续的价格。
+ 后复权，即以今天的价格为基础，根据复权因子调整之前的价格

在JAQS里面，只需要使用adjust_mode参数，设置成'post'(后复权)或'pre'(前复权)，系统会自动进行复权处理。

## 如何利用quantOS构建自己的行情系统

主要包括两部分：

(1) 实时行情：quantOS提供DataCore项目，支持对接ctp期货行情和sina、tencent股票行情，qms实时合成分钟线，并保留所有的tick数据。DataServer统一对外提供实时行情和分钟线服务。
(2) 历史行情：每日日终，使用tk2bar工具，可以将tick数据转化成分钟线，并通过DataServer对外提供服务。

逻辑架构图如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case5-5.png)

详细信息请登录www.quantos.org索取。


