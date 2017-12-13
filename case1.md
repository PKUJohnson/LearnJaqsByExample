# case 1：初识A股

我国股票市场诞生于1991年，已经有近30年的历史。对于中国股市，不同年代的股民有着不同的认识。

有人始终认为中国股市是一个大赌场，也有越来越多的人认为中国股市已经非常接近现代资本市场。

这篇文章，我们从量化的角度看看2017年的中国A股（B股太小，新三板不够透明，这里就不研究了）。

从几个问题出发：（如果你想直接撸代码，请访问[这里](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case1.ipynb)）

## 1. 你知道中国A股有多少只股票吗？

直接上代码，JAQS中提供了全部的证券标的基本信息，如下：
```python
from jaqs.data import DataApi
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd
import numpy as np

api = DataApi(addr='tcp://data.tushare.org:8910')
phone = 'phone'
token = 'token'
df, msg = api.login(phone, token)
print(df, msg)

# inst_type = 1   表示股票
# status = 1      表示股票正常交易，未退市
# market = SH,SZ  取上海和深圳的股票

df, msg = api.query(
    view="jz.instrumentInfo",
    fields="market,symbol,list_date,status",
    filter="inst_type=1&status=1&market=SH,SZ",
    data_format='pandas')

df.index = df['symbol']
df.sort_index(inplace=True)

print(len(df))
print(len(df[df['market']=='SZ']))
print(len(df[df['market']=='SH']))
```
正确结果：
截至到2017年12月11日，沪深股市股票共3454只，其中深圳2070只，上海1384只。

## 2. 你知道A股的股票是怎么发行出来的吗？股票发行和股市走势有关系吗？与证监会换届有关系吗？

JAQS刚好可以取出所有股票的发行日期，我们按照月度统计，看看股票发行数量的分布情况。

```python
list_date = df['list_date'].astype(int)
ser_year = list_date // 10000

year_month = list_date // 100

gp = df.groupby(by=year_month)
count = gp.count().iloc[:, 0]

year_month_full = [year * 100 + month for year in range(ser_year.min(), ser_year.max()+1) for month in range(1, 13)]

count = count.reindex(year_month_full).fillna(0).astype(int)
count.tail()
```

取出上证指数的日线，计算上证指数的走势
```python
df_daily, msg = api.daily('000001.SH', df['list_date'].min(), df['list_date'].max())
df_daily = df_daily.set_index('trade_date')
df_daily.tail()
```

附加上证监会换届情况
```python
presidents = {
 'SFL': 20021201,
 'GSQ': 20111029,
 'XG': 20130318,
 'LSY': 20160220
}

presidents_dt = {k: pd.to_datetime(v, format="%Y%m%d") for k, v in presidents.items()}
presidents_dt
```

将几张图叠加在一起，可以看到还是有一些规律的
```python
plt.rcParams.update({'font.size': 14})

fig, ax1 = plt.subplots(figsize=(16, 5))
ax2 = ax1.twinx()

start_time = 200201
start_time_day = start_time * 100 + 1

idx = count.loc[start_time:].index
idx0 = list(range(len(idx)))
ipo = count.loc[start_time:].values
ser_price = df_daily.loc[start_time_day:]['close']
price = ser_price.values
price_idx = [idx.get_loc(x // 100) + (x % 100) / 31. for x in ser_price.index]



ax1.bar(idx0, ipo, width=.6)
ax1.set(xlabel='Date', ylabel='Number of IPO', title='Index v.s. IPOs',
        xlim=(idx0[0] - 2, idx0[-1] + 2),
        xticks=idx0[::12])


ax2.plot(price_idx, price, color='orange')
ax2.set(ylabel='000001.SH')

ipo_max = np.max(ipo)
y_ = ipo_max * .9
for name, debut_time in presidents.items():
    x_ = idx.get_loc(debut_time // 100)
    ax1.axvline(x_, color='indianred', linestyle='--')
    ax1.annotate(s=name, xy=(x_, y_))

ax1.xaxis.set_major_formatter(MyFormatter(idx, '%Y'))
```

我们得到的图形如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case1.png)

## 3. 你知道今年中国A股每支股票的收益情况吗？A股今年涨幅最大的股票都是谁？

我们选取2016年12月30日为基准日，看看A股今年的收益情况。

```python
start_date = 20161230
end_date   = 20171130

df_symbols = ",".join(df.index)
print(df_symbols)

# 获取日行情 start_date
df_daily_start, msg = api.daily(df_symbols, start_date, start_date)
df_daily_start = df_daily_start.set_index('symbol')
df_daily_start.head()

# 获取日行情 end_date
df_daily_end, msg = api.daily(df_symbols, end_date, end_date)
df_daily_end = df_daily_end.set_index('symbol')
df_daily_end.head()

# 获取复权因子 start_date
filter="symbol=" + df_symbols + "&start_date=" + str(start_date) + "&end_date=" + str(start_date)

df_adjfactor_start, msg = api.query(
                  view="lb.secAdjFactor",
                  fields="",
                  filter=filter,
                  data_format='pandas')

df_adjfactor_start = df_adjfactor_start.set_index('symbol')
df_adjfactor_start = df_adjfactor_start['adjust_factor'].astype('float')

# 获取复权因子 end_date
filter="symbol=" + df_symbols + "&start_date=" + str(end_date) + "&end_date=" + str(end_date)

df_adjfactor_end, msg = api.query(
                  view="lb.secAdjFactor",
                  fields="",
                  filter=filter,
                  data_format='pandas')

df_adjfactor_end = df_adjfactor_end.set_index('symbol')
df_adjfactor_end = df_adjfactor_end['adjust_factor'].astype('float')

# 计算个股收益率

df_return = (df_daily_end['close'] * df_adjfactor_end) / (df_daily_start['close'] * df_adjfactor_start) - 1.0
df_return = df_return.sort_values().dropna()

fig, ax1 = plt.subplots(1, 1, figsize=(10, 4))
ax1.hist(df_return, bins=200)
ax1.set(xlabel='Return', ylabel='Number', title='Return List')
fig.show()

# 统计指标
df_return.describe()

# 中位数
np.median(df_return)
```

我们可以看到，今年的股票收益分布情况如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case1-2.png)

|统计指标|          值|
|--------|------------|
|median  |   -0.189635|
|mean    |   -0.122894|
|std     |    0.326354|
|min     |   -0.708213|
|25%     |   -0.324713|
|50%     |   -0.189635|
|75%     |   -0.016754|

+ 均值统计是-12%，中位数是-19%，75%分位的股票都在赔钱。
+ 最惨的赔了70%（002070.SZ ST众和）
+ 最牛的涨了320%（601313.SH江南嘉捷），360借壳标的，你懂的。

让我们再剔除次新股，我们看看今年真正的好股票是那些。

```python
# 选出今年涨幅超过80%的股票，但剔除次新股
df_return = df_return[(df_return>0.8)&(df_return < 5)]

sel_symbol = ",".join(df_return.index)

df, msg = api.query(
                view="jz.instrumentInfo",
                fields="status,list_date, fullname_en, market",
                filter="inst_type=1&status=1&symbol="+sel_symbol,
                data_format='pandas')

df = df.set_index('symbol')
df['return'] = df_return

df = df[df['list_date'].astype(int)<20160101]

df.sort_values('return')
```

结果表明，今年真的是大盘白马股的天下。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case1-3.png)


## 4. 想尝试一下？

请访问www.quantos.org，下载安装JAQS，开始自己的量化旅程吧。

这里的东西都是开源和免费的。

