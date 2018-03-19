# 数字货币量化交易基础（1）

## 快速获取数字货币的行情和交易信息

随着比特币的暴涨暴跌，人们对数字货币的关注程度越来越高，有一些人开始关注数字货币的量化交易。
量化交易的基础是获取市场数据，包括行情、K线、历史成交等，如何才能通过程序快速获取数字货币的市场数据呢？

数字货币的交易可以在各个交易所进行，因此每个交易所都有自己的行情API。
作者选取了火币网的API，并包装成了python类，方便普通用户使用。

火币网API地址：[https://github.com/huobiapi/API_Docs/wiki](https://github.com/huobiapi/API_Docs/wiki)

封装后的Python API代码地址：[https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/huobi_agent.py](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/huobi_agent.py)

## 主要API及其使用方法

```python
# import library
from huobi_agent import HuobiAgent

agent = HuobiAgent()

# symbol includes (btcusdt, bchusdt, ltcusdt, ethusdt)
# 'btcusdt' -> 比特币美元
# 'bchusdt' -> 比特币现金美元
# 'ltcusdt' -> 莱特币美元
# 'ethusdt' -> 以太币美元

# api format 
# df, msg = agent.func(params)
# 如果df is None，则看msg错误信息

# 获取实时行情
df, msg = agent.get_quote('btcusdt')

# 获取K线信息
# 类型: 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
# 不能超过2000条
df, msg = agent.get_kline('btcusdt', '1day', 2000)

# 获取市场深度信息
df, msg = agent.get_market_depth('btcusdt', 'step1')

# 获取成交信息
df, msg = agent.get_trade('btcusdt')

# 获取历史成交信息
df, msg = agent.get_hist_trade('btcusdt')
```

## 使用Example

本例子展示通过获取数字货币日线数据并画出价格走势图。

```python
def draw_plot(agent, symbol, ax):
    # 获取数据
    df, msg = agent.get_kline(symbol, '1day', 2000)
    # 画柱状图
    ax.plot(df.index, df['close'])

    # 标识标题及坐标轴信息
    ax.set_title('huobi pro close price of ' + symbol)
    ax.set_xlabel('time')
    ax.set_ylabel('huobi pro close price of ' + symbol)    

# 导入python画图库matplotlib
import matplotlib.pyplot as plt  

# 设置图片大小
fig = plt.figure(figsize=(16,10))
agent = HuobiAgent()

ax = fig.add_subplot(2, 2, 1)
draw_plot(agent, 'btcusdt', ax)

ax = fig.add_subplot(2, 2, 2)
draw_plot(agent, 'bchusdt', ax)

ax = fig.add_subplot(2, 2, 3)
draw_plot(agent, 'ethusdt', ax)

ax = fig.add_subplot(2, 2, 4)
draw_plot(agent, 'ltcusdt', ax)

# arrange layout
plt.tight_layout()

# 显示画图结果
plt.show()
```

图片显示结果如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/huobi.png)


