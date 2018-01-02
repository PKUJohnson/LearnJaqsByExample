# case 7：JAQS策略框架探密(1) - 初识alpha策略框架

JAQS提供两大类的策略模板
+ alpha选股策略
+ 行情驱动的选股策略

作者将通过一系列的策略样例，逐渐打开JAQS策略系统的神秘面纱。本文是第一篇：初识alpha策略框架。

## Alpha策略框架及JAQS实现

一个专业且严谨的alpha股票策略的研究流程如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/alpha_workflow.png)

主要包括5个步骤：
+ 1.数据的获取
+ 2.投资范围Universe的确定
+ 3.Alpha信号的生成
+ 4.投资组合构建（优化目标、风险模型、约束）
+ 5.交易执行

JAQS系统的alpha框架完整的包含了上述几个模块：

+ 数据：使用DataView组件，支持使用公式定义衍生数据
+ Universe：可以通过指数定义universe，支持对universe通过stock_selector进行条件过滤
+ Alpha信号：用户可以自定义alpha信号
+ 投资组合构建：支持等权重、市值权重等构建方法，优化权重正在开发中
+ 交易执行：提供回测撮合引擎

## Alpha策略样例

下面我们通过一个简单的例子，说明如何使用JAQS进行策略回测。策略idea如下：

**我们从沪深300中选取优质资产回报的股票，剔除次新股，按照等权重的方法进行投资，看看其与hs300指数的表现谁更好。**

上述这个策略idea，使用alpha框架分解和细化一下，我们得到：

+ universe限定在hs300范围内
+ 股票的年化ROE大于某个限定值（净资产回报）
+ 股票的年化ROA大于某个限定值（总资产回报）
+ 股票非次新股，上市时间不小于一年

在JAQS里面，几个组件配合起来，就可以顺利的完成上述要求：

+ DataView：限定universe=000300.SH，原始数据包括年化ROA，年化ROE
+ 标的集过滤：年化ROA>阈值，年化ROE>阈值，非次新股
+ 组合构建：符合条件的标的范围内，等权重投资
+ Alpha信号：不需要

### 小知识：了解 ROE 和 ROA

ROE：净资产收益率ROE(Rate of Return on Common Stockholders’ Equity) = 净利润 / 平均股东权益

ROA：资产收益率（Return on Assets，ROA）= 净利润 / 总资产

这两个指标都是反映公司资产回报率的。

## Alpha策略代码

```python

data_config = {
  "remote.data.address": "tcp://data.tushare.org:8910",
  "remote.data.username": "phone",
  "remote.data.password": "token"
}

trade_config = {
  "remote.trade.address": "tcp://data.tushare.org:8910",
  "remote.trade.username": "phone",
  "remote.trade.password": "token"
}

dataview_folder = './data'
backtest_result_folder = './backtest'

start_date = 20160101
end_date   = 20171229

universe  = '000300.SH'
benchmark = '000300.SH'
```
这段代码主要定义了常用的变量，包括data_config, trade_config, 回测时间段，投资标的和业绩基准等

```python
# setp1: load and save data for research
def save_dataview():
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    dv = DataView()
    
    props = {'start_date': start_date, 
			 'end_date': end_date, 
			 'universe': universe,
             'fields': 'roe_yearly,roa_yearly',
             'freq': 1}
    
    dv.init_from_config(props, ds)
    dv.prepare_data()
    
	# add derived data by formula
    dv.add_formula('roe_cond', 'roe_yearly >= 20', is_quarterly=True)
    dv.add_formula('roa_cond', 'roa_yearly >= 5', is_quarterly=True)
    dv.add_formula('cond', 'roe_cond && roa_cond', is_quarterly=True)
    
    dv.save_dataview(folder_path=dataview_folder)
```
这段代码用于加载数据，代码非常直接：
+ 从基础数据中获取roe_yearly,roa_yearly这两个指标，freq=1表示每日数据
+ 通过add_formula产生出衍生指标，is_quarterly=True表示数据是季度更新，系统自动扩展到每日数据
+ 系统在扩展季度数据到每日的时候，会考虑数据的point-in-time问题，避免look-ahead bias（未来函数）
+ 将DataView获取的数据保存到本地，供后面的回测使用。（**可以反复使用**）

DataView具有非常强大的数据处理能力，具体的用法，请参看[DataView使用说明](https://github.com/quantOS-org/JAQS/blob/master/doc/data_view.md)

后面的系列文章里，我们会找机会全面介绍DataView。

```python
# step2: define a stock selector
def selector_roe_roa_not_new(context, user_options=None):
    snapshot = context.snapshot
    
    cond = snapshot['cond']
    
    df_inst = context.dataview.data_inst
    new_mask = context.trade_date - df_inst['list_date'] <= 10000
    new_stocks = new_mask.loc[new_mask].index
    cond.loc[new_stocks] = 0.0
    
    return cond	
```
这段代码定义了一个universe选择器，它从满足roe和roa条件的证券列表中，去掉上市时间不超过1年的股票。

+ context是alpha策略的上下文，里面保存了所有策略相关的信息，例如DataView
+ context.snapshot是当前数据的快照
+ context.dataview.data_inst是一个DataFrame，保存了所有的instrument信息
+ data_inst['list_date]是股票的上市时间
+ context.trade_date是当前的交易日，即回测发生的日期

```python
# step3: backtest function
def alpha_strategy_backtest():
    dv = DataView()

    dv.load_dataview(folder_path=dataview_folder)
    
    props = {
        "benchmark": benchmark,
        "universe": ','.join(dv.symbol),
    
        "start_date": dv.start_date,
        "end_date": dv.end_date,
    
        "period": "month",
        "days_delay": 0,
    
        "init_balance": 1e8,
        "position_ratio": 1.0,
        }
    props.update(data_config)
	props.update(trade_config)

    trade_api = AlphaTradeApi()
    trade_api.init_from_config(props)

    stock_selector = model.StockSelector()
    stock_selector.add_filter(name='selector_roe_roa_not_new', func=selector_roe_roa_not_new)

    strategy = AlphaStrategy(stock_selector=stock_selector, pc_method='equal_weight')
    pm = PortfolioManager()

    bt = AlphaBacktestInstance()

    context = model.Context(dataview=dv, instance=bt, strategy=strategy, trade_api=trade_api, pm=pm)
    stock_selector.register_context(context)

    bt.init_from_config(props)
    bt.run_alpha()

    bt.save_results(folder_path=backtest_result_folder)
```
这是回测的核心代码，主要做了几件事：
+ 将DataView的数据从本地加载进来
+ 定义了一个投资标的过滤器model.StockSelector
+ 定义了一个AlphaStrategy的策略实例
+ 定义了一个AlphaBacktestInstance回测实例
+ 定义了一个PortfolioManager组合管理实例
+ 定义了一个AlphaTradeApi模拟撮合实例
+ 通过model.Context，将DataView, AlphaStrategy, AlphaBacktestInstance, PortfolioManager, AlphaTradeApi关联起来
+ 通过AlphaBacktestInstance.run_alpha()进行回测
+ 将回测结果保存到本地，供后续分析使用

```python	
# backtest analyze
def backtest_analyze():
    ta = ana.AlphaAnalyzer()
    dv = DataView()
    dv.load_dataview(folder_path=dataview_folder)
    
    ta.initialize(dataview=dv, file_folder=backtest_result_folder)

    ta.do_analyze(result_dir=backtest_result_folder, selected_sec=list(ta.universe)[:3])
```
这段代码是分析模块，将之间的数据和回测结果加载后，直接进行分析。

```python	
# main function
if __name__ == "__main__":
    t_start = time.time()
    
    save_dataview()
    alpha_strategy_backtest()
    backtest_analyze()
    
    t3 = time.time() - t_start
    print("\n\n\nTime lapsed in total: {:.1f}".format(t3))
	
'''
这段代码是主函数，将上述流程组织起来。

## Alpha策略回测结果

回测包括几个部分：

1. pnl曲线

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/7-1.png)

2. 策略表现指标，包括相对年化收益，年化波动率，sharpe比率，Beta，最大Drawdown等

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/7-2.png)

3. 详细的交易信息，可作为策略运行正确性的验证，都保存在文件中。如下表：

|文件名             |        内容|
|-------------------|------------|
|daily_position.csv |每日持仓信息|
|trades.csv         |全部交易信息|
|returns.csv        |每日盈亏信息|
|report.html        |回测报告    |

## Alpha策略进阶讨论

在JAQS中实现Alpha策略，你实际上只需要实现模块中的内容即可，非常方便。主要模块包括：

+ 用DataView获取数据，保存在本地
+ 定义投资标的集和进一步的过滤条件
+ 定义信号及信号组合
+ 构建资产组合

目前系统已实现如equal_weight, market_value_weight等权重方案，未来会加入risk_parity, optimizer等复杂方案。

在这里，Alpha信号不是必须的，如本例未使用。

后面的系列文章里，我们将介绍如何利用Alpha信号，构建投资组合。

