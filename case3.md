# case 3：认识指数增强型基金

本案例中，我们分析一下A股的指数增强型股票基金在2017年的业绩表现。

如果你想直接撸代码，请访问[这里](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case3.ipynb)

## 1. 定义

指数增强型基金的定义如下：

指数增强型基金并非纯指数基金，是指基金在进行指数化投资的过程中，
为试图获得超越指数的投资回报，在被动跟踪指数的基础上，加入增强型的积极投资手段，
对投资组合进行适当调整，力求在控制风险的同时获取积极的市场收益。

因此，指数增强型基金一般有一个指数作为业绩基准。

## 2. 如何评价一个指数增强型基金的业绩表现

一般而言，主要看几个方面：

+ active return，即相对于指数的主动管理收益
+ active volatility，主动收益的波动性
+ sharpe ratio，主动管理的夏普率
+ beta，即与跟踪指数间的相关性。（越接近1越好）

当然，用户也会关心基金的绝对收益，最大回撤等指标。

## 3. 如何在JAQS中进行分析

主要分为几个步骤：

1. 取出符合条件的股票型基金中的指数增强基金，代码如下:

```python

# 分级A需要去掉
def get_fundlist(api, invest_type, invest_style):
    df, msg = api.query(
                view="lb.mfInfo",
                fields="invest_type,invest_style,status",
                filter="",
                data_format='pandas')
    
    #print(df, msg)
    
    df = df[(df['invest_type'] == invest_type) 
            & (df['invest_style'] == invest_style) 
            & (df['status'] == 101001000) 
            & (df['name'].apply(lambda s: 'A' not in s))]
    
    return df

df = get_fundlist(api, u'股票型', u'增强指数型')
	
```

2. 取出每支基金对应的指数信息，代码如下：

```python
def get_fundnav(api, symbol, start_date, end_date):
    df, msg = api.query(
        view="lb.mfNav",
        fields="price_date, nav_adjusted",
        filter="start_pdate=" + str(start_date) + "&end_pdate=" + str(end_date) + "&symbol=" + symbol,
        data_format='pandas'
    )
    
    if df is None:
        print(df, msg)
    
    df.index = df['price_date'].astype(np.integer)
    df.sort_index(inplace=True)
    return df

start_date = 20161230
curr_date  = 20171215

index_map = get_index_map(api, symbols, start_date)	
```

3. 取出基金的历史净值和指数的历史价格信息，注意需要用复权因子矫正后的净值。代码如下：
```python
def get_fundnav(api, symbol, start_date, end_date):
    df, msg = api.query(
        view="lb.mfNav",
        fields="price_date, nav_adjusted",
        filter="start_pdate=" + str(start_date) + "&end_pdate=" + str(end_date) + "&symbol=" + symbol,
        data_format='pandas'
    )
    
    if df is None:
        print(df, msg)
    
    df.index = df['price_date'].astype(np.integer)
    df.sort_index(inplace=True)
    return df

def get_index_daily(api, symbol, start, end):
    
    df, msg = api.daily(
                    symbol=symbol,
                    fields="",
                    start_date=start,
                    end_date=end,
                    data_format='pandas')

    if df is None:
        print(df, msg)
    
    df.index = df['trade_date']
    df.sort_index(inplace=True)
    
    return df	
```

4. 计算每支基金的管理绩效，包括active return, active volatility, sharpe ratio, beta, MaxDrawDown等。

```python
def cal_active_return(api, symbol, bench, start, end):

    df_nav = get_fundnav(api, symbol, start, end)
    df_idx = get_index_daily(api, bench, start, end)
    
    if df_idx.empty or df_nav.empty:
        return None, None, None 
    
    strategy_value = df_nav['nav_adjusted']
    bench_value = df_idx['close']
    
    market_values = pd.concat([strategy_value, bench_value], axis=1).fillna(method='ffill')
    market_values.columns = ['strat', 'bench']
    
    df_returns = market_values.pct_change(periods=1).fillna(0.0)
    
    df_returns = df_returns.join((df_returns.loc[:, ['strat', 'bench']] + 1.0).cumprod(), rsuffix='_cum')

    df_returns.loc[:, 'active_cum'] = df_returns['strat_cum'] - df_returns['bench_cum'] + 1
    df_returns.loc[:, 'active'] = df_returns['active_cum'].pct_change(1).fillna(0.0)

    start = pd.to_datetime(start, format="%Y%m%d")
    end = pd.to_datetime(end, format="%Y%m%d")
    years = (end - start).days / 365.0
    
    active_cum = df_returns['active_cum'].values
    max_dd_start = np.argmax(np.maximum.accumulate(active_cum) - active_cum)  # end of the period
    max_dd_end = np.argmax(active_cum[:max_dd_start])  # start of period
    max_dd = (active_cum[max_dd_end] - active_cum[max_dd_start]) / active_cum[max_dd_start]

    performance_metrics = dict()

    performance_metrics['Annual Return (%)'] =\
        100 * (np.power(df_returns.loc[:, 'active_cum'].values[-1], 1. / years) - 1)
    performance_metrics['Annual Volatility (%)'] =\
        100 * (df_returns.loc[:, 'active'].std() * np.sqrt(242))
    performance_metrics['Sharpe Ratio'] = (performance_metrics['Annual Return (%)']
                                                / performance_metrics['Annual Volatility (%)'])
    
    risk_metrics = dict()
    
    risk_metrics['Beta'] = np.corrcoef(df_returns.loc[:, 'bench'], df_returns.loc[:, 'strat'])[0, 1]
    risk_metrics['Maximum Drawdown (%)'] = max_dd * 100
    risk_metrics['Maximum Drawdown start'] = df_returns.index[max_dd_start]
    risk_metrics['Maximum Drawdown end'] = df_returns.index[max_dd_end]
    
    return performance_metrics, risk_metrics, df_returns
```

5. 将上述函数按流程组织在一起，计算出所有符合条件的基金的管理绩效，如下

```python
api = DataApi('tcp://data.tushare.org:8910')

username = "phone"
password = "token"

df, msg = api.login(username, password)
print(df, msg)

df = get_fundlist(api, u'股票型', u'增强指数型')

symbols = ",".join(df['symbol'])

start_date = 20161230
curr_date  = 20171215

index_map = get_index_map(api, symbols, start_date)

print(index_map)

indicators = list()

for (symbol, index) in index_map.items():

    performance_metrics, risk_metrics, df_returns = cal_active_return(api, symbol, index, start_date, curr_date)

    if performance_metrics is None:
        continue

    indicators.append((symbol, 
                       index, 
                       performance_metrics['Annual Return (%)'],
                       performance_metrics['Annual Volatility (%)'],
                       performance_metrics['Sharpe Ratio'],
                       df_returns['strat_cum'].iat[-1],
                       df_returns['bench_cum'].iat[-1],
                       risk_metrics['Beta'],
                       risk_metrics['Maximum Drawdown (%)'],
                       risk_metrics['Maximum Drawdown start'],
                       risk_metrics['Maximum Drawdown end'])
                    )

labels = ['symbol', 'index', 'AnnualReturn', 'AnnualVolatility', 'SharpeRatio', 'StratCumReturn', 'BenchCumReturn', 'Beta', 'MaximumDrawdown', 'MaximumDrawdownStart', 'MaximumDrawdownEnd']

df = pd.DataFrame.from_records(indicators, columns=labels)

df.describe()

df = df.sort_values('SharpeRatio')

df.sort_values('AnnualReturn')

```

注意，期间可能需要手工去掉几个基金名称里面不带A的分级A。

运行之后，我们得到如下的结果。[case3.xls](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case3.xls)

可以得出几个明显的结论：

1. 指数增强基金的管理还是**卓有成效**的，从中位数看，基金经理取得的成绩是：

AnnualReturn：2.92%，SharpeRatio：1.21，Beta：0.97

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-1.png)

2. 增强指数基金的业绩也是有分化的。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-2.png)

**_表现最好的三只基金及其收益情况_**

|symbol    |index     |AnnualReturn|AnnualVolatility|SharpeRatio|
|------    |-----     |------------|----------------|-----------|
|150136.SZ |000903.SH |	53.28 	   |16.34 	        |3.26       | 
|003647.OF |000852.SH |	14.99 	   |2.63 	        |5.70       | 
|002316.OF |000905.SH |	11.04 	   |3.18 	        |3.47       | 

增强收益都超过了11%，sharpe比率超过3。

**_表现最差的三只基金及其收益情况_**

|symbol    |index     |AnnualReturn|AnnualVolatility|SharpeRatio|
|------    |-----     |------------|----------------|-----------|
|450008.OF |000300.SH |	-6.63      |	3.82 	    |-1.74      | 
|150139.SZ |000842.SH |	-6.64      |	15.36 	    |-0.43      | 
|410010.OF |399005.SZ |	-8.42      |	3.00 	    |-2.81      | 

增强收益都超过了-6.6%，sharpe比率也很低。

150136.SZ(国富100B)很有意思，其与基准的之间的比较图如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-3.png)

其大幅跑赢中证100指数，超额收益超过年化53%。作者试图寻找其中的原因，将其业绩回溯到更早的区间，发现了其中的一点点线索：

如果将时间回溯到150136.SZ成立的2015年3月，其整个业绩表现是不如指数的，如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-4.png)

2016年5月新增加一名基金经理之后，业绩开始大幅回升，特别是2016年9月份之后，业绩一路超过基准。如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-5.png)

看来新基金经理的作用还是很明显的。

另一个值得表扬的基金经理是003647.OF（创金合信中证1000），其业绩表现如下图：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case3-6.png)

在今年中证1000大幅下跌超过10%的情况下，力保本基金只小幅亏损，也算是大功一件。

至于410010.OF（华富中小板），虽然你也取得了9%的收益，但指数上涨了17%，是不是应该反思一下呢？

## 5. 想尝试一下？

请访问www.quantos.org，下载安装JAQS，开始自己的量化旅程吧。

这里的东西都是开源和免费的。
