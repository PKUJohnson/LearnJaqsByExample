# case 7：JAQS策略框架探密(1) - 初识行情驱动的策略框架

JAQS提供两大类的策略模板
+ alpha选股策略
+ 行情驱动的策略框架

本文是第二篇：初识行情驱动策略框架。

这里是全部的[源代码](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case8.py)

## 行情驱动策略框架及JAQS实现

行情驱动的策略工作流如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/eventdriven_workflow.png)

其工作流程如下：

+ 1.通过行情源产生行情事件队列。
+ 2.策略从事件队列取出并处理行情事件，计算并产生交易信号。
+ 3.策略将交易发送到交易系统或者回测系统。
+ 4.交易系统或回测系统撮合成交后，将成交事件发送到事件队列。
+ 5.策略处理成交事件，更新委托持仓信息。

JAQS系统的alpha框架完整的包含了上述几个模块：

+ 数据源：使用RemoteDataService组件，可以获取实时或历史数据
+ 策略模板：提供EventDrivenStrategy基础类，用户继承后实现自己的业务逻辑即可。
+ 交易模块：BacktestTradeApi是回测类，RealTimeTradeApi是实盘类。
+ 组合管理：提供一个默认的PortfolioManager类，可以处理绝大部分的成交事件和持仓管理逻辑。

## 行情驱动的策略样例

下面我们通过一个简单的例子，说明如何使用JAQS进行行情驱动的策略开发和回测。策略idea如下：

一个双均线的技术指标策略，10日均线与20日均线交叉，标的为510300.SH，
+ 如果10日均线上穿20日均线，则买入固定数量的510300.SH
+ 如果10日均线下穿20日均线，且已有持仓，则卖出所有数量的510300.SH

## 行情驱动策略代码

第一部分，继承EventDrivenStrategy类，并实现行情处理的逻辑

```python

class DoubleMaStrategy(EventDrivenStrategy):

    def __init__(self):
        super(DoubleMaStrategy, self).__init__()

    def init_from_config(self, props):
        """
        将props中的用户设置读入
        """
        super(DoubleMaStrategy, self).init_from_config(props)
	
	def on_bar(self, quote_dic):
        """
		行情处理逻辑写在这里
        """	
		pass

    def on_trade(self, ind):
        """
		成交处理逻辑写在这里
        """
		pass
```
具体实现逻辑比较繁琐，基本思想就是：
+ 每个行情到达时，计算10日均线和20日均线。
+ 如果10日均线上穿，则产生买入信号，买入固定数量的证券。
+ 如果10日均线下穿，则产生卖出信号。此时如果有持仓，则全数卖出。

细节代码可以参考源代码。


第二部分，组织回测流程

```python

def run_strategy():
    """
    回测模式
    """
    props = {"symbol": '510300.SH',
             "start_date": 20160201,
             "end_date": 20171231,
             "fast_ma_length": 10,
             "slow_ma_length": 20,
             "bar_type": "1d",
             "benchmark" : '000300.SH',
             "init_balance": 50000}
	
	# 回测交易的API
    tapi = BacktestTradeApi()
	
	# 回测引擎
    ins = EventBacktestInstance()
        
    props.update(data_config)
    props.update(trade_config)
    
	# 行情事件源
    ds = RemoteDataService()
    strat = DoubleMaStrategy()
    pm = PortfolioManager()

	# 策略运行上下文
    context = model.Context(data_api=ds, trade_api=tapi, instance=ins,
                            strategy=strat, pm=pm)
    
    ins.init_from_config(props)

	# 回测执行
    ins.run()

    ins.save_results(folder_path=result_dir_path)
```

第三部分，分析回测结果
```python
def analyze():
    ta = ana.EventAnalyzer()
    
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    
    ta.initialize(data_server_=ds, file_folder=result_dir_path)
    
    ta.do_analyze(result_dir=result_dir_path, selected_sec=[])
```

第四部分，put all together
```python	
# main function
if __name__ == "__main__":
    run_strategy()
    analyze()	
```

## 策略回测结果

回测包括几个部分：
1. pnl曲线
2. 策略表现指标，包括相对年化收益，年化波动率，sharpe比率，Beta，最大Drawdown等
3. 详细的交易信息，可作为策略运行正确性的验证，都保存在文件中。如下表：

这个与之前的Alpha策略相同，不再赘述，感兴趣的可以看看之前的那篇文章(https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/case7.md)。
