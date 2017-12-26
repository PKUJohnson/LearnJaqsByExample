# case 6：详解TradeSim仿真交易系统

TradeSim仿真交易系统在策略开发过程中至关重要，可以用于策略实盘前的验证，与实盘效果十分接近。

TradeSim是一套为专业投资机构设计的交易平台，一般投资者在使用过程中可能会遇到一些问题，产生一些疑惑，本文将详解其中的设计思想。

## TradeSim的访问方式

有三种方式可以访问TradeSim：

+ (1) 通过TradeApi进行程序化交易和查询
+ (2) 通过vnTrader连接TradeSim进行交易和查询
+ (3) 通过仿真交易网页[https://www.quantos.org/tradesim/trade.html](https://www.quantos.org/tradesim/trade.html)进行查询

### TradeApi的使用

TradeApi是程序化接口，用户在策略中可以调用TradeApi直接进行交易。TradeApi包括如下几大功能：

```python
from jaqs.trade.tradeapi import TradeApi

# 登录
tapi = TradeApi(addr="tcp://gw.quantos.org:8901") 
user_info, msg = tapi.login("phone", "token")     

# 选择策略号
tapi.use_strategy(123) # 123为给你分配的策略号，可以从user_info中获得

# 查询账户信息
df, msg = tapi.query_account()

# 查询可投资标的信息
df, msg = tapi.query_universe()

# 查询Portfolio, 返回当前的策略帐号的Universe中所有标的的净持仓，包括持仓为0的标的
df, msg = tapi.query_portfolio()

# 查询当前策略帐号的所有持仓,和 query_portfolio接口不一样。
# 如果莫个期货合约 Long, Short两个方向都有持仓，这里是返回两条记录 返回的 size 不带方向，全部为正
df, msg = tapi.query_position()

# 单标的下单
task_id, msg = tapi.place_order("000025.SZ", "Buy", 57, 100, algo, algo_param)

# 撤单
tapi.cancel_order(task_id)

# 查询委托
df, msg = tapi.query_order(task_id = task_id, format = 'pandas')

# 查询成交
df, msg = tapi.query_trade(task_id = task_id, format = 'pandas')

# 目标持仓下单
portfolio, msg = tapi.goal_portfolio(goal, algo, algo_param)

# portfolio撤单
tapi.stop_portfolio()

# 批量下单(1) place_batch_order，指定绝对size和交易类型
orders = [ 
    {"security":"600030.SH", "action" : "Buy", "price": 16, "size":1000},
    {"security":"600519.SH", "action" : "Buy", "price": 320, "size":1000},
    ]

task_id, msg = tapi.place_batch_order(orders)

# 批量下单(2) basket_order，指定变化量，不指定交易方向，由系统根据正负号来确定
orders = [ 
    {"security":"601857.SH", "ref_price": 8.40, "inc_size":1000},
    {"security":"601997.SH",  "ref_price": 14.54, "inc_size":20000},
    ]

task_id, msg = tapi.basket_order(orders)
```

这里有几个非常重要的概念，如图：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case6-1.png)

+ 仿真交易系统会为每个账户自动分配三个Strategy，这里的Strategy是一个交易Book的编号，用于管理持仓和交易。
+ 每个Strategy对应有一个Universe，即可投资的标的范围，如中证500或沪深300，专业投资一般都会限定投资范围，不能超出范围投资。

这是典型自营交易机构的业务架构，可支持多交易员进行交易。

在API的下单方式上，我们提供：

+ 单标的下单（place_order）
+ 一篮子下单（place_batch_order，basket_order）
+ 目标持仓下单（goal_portfolio）

其中的下单方式，又支持两个特性：

+ 使用绝对数量下单和变化量下单（action + size，inc_size）
+ 普通下单和使用算法下单（algo，algo_param）

目标持仓下单是一种调仓的交易方式，即将当前持仓调整成目标持仓，系统会自动生成相应的差异订单。
当前的持仓可以通过query_portfolio查询。

### TradeApi常见问题

用户在使用TradeApi进行仿真交易时，常常遇到一些问题，这里详细解答

+ Q: 如何获取我的策略号？
+ A: 登录成功后，系统自动返回策略信息
```python
user_info, msg = tapi.login("phone", "token")     
print(user_info['strategies'])
accounts = user_info['accounts']
for (key, value) in accounts.items():
    print(u"%s, %s" % (key, value))
```
系统会返回：
```
[1008, 1009, 1010, 3919]
1010, 股指期货
3919, 商品期货
1009, 中证500
1008, 沪深300
```

+ Q: 调用返回 -1,NO PRIVILEGE
+ A: 这是由于use_strategy没有使用正确的strategy_no.
```python
df, msg = api.use_strategy(1)
```
详见上面的问题“如何获取我的策略号”

+ Q: 调用返回 -1,000025.SZ not in UNIVERSE
+ A: 这是由于你使用的标的不在Universe范围内，属于超投资范围的标的，不允许下单。可以通过query_universe接口查询可投资标的。

+ Q: 调用返回 -1,risk rule violated: inst[10063] rule[1] expects price_diff[0.86152841280209] <= 0.03
+ A: 下单价格超出风控范围。系统目前自动设置了一个3%的涨跌幅限制，任何超过当前最新价3%的委托，都会被拒绝

+ Q: 如何判断下单成功了
+ A: 返回了TaskID，表明下单成功。TaskID是一个长整数，例如：10081226000039L

### 撮合机制

撮合是仿真交易的核心模块，目前采取的撮合机制是按实时价格进行撮合，工作原理如下：

+ 撮合引擎监控每个市场tick，根据tick的最新价，对发送到系统的未成交委托进行模拟撮合。
+ 如果最新价和订单可以成交，则生成成交记录，并更新订单信息。
+ 目前的撮合不考虑成交量的影响，未来会继续改进。

### 成交推送

+ TradeSim通过TradeApi提供完备的推送事件，助力策略提高响应效率。
+ TradeApi通过回调函数方式通知用户事件。事件包括三种：订单状态、成交回报、委托任务执行状态。

- 订单状态推送
```python
def on_orderstatus(order):
    print "on_orderstatus:" #, order
    for key in order:    
        print "%20s : %s" % (key, str(order[key]))
```

- 成交回报推送
```python
def on_trade(trade):
    print "on_trade:"
    for key in trade:    
        print "%20s : %s" % (key, str(trade[key]))
```

- 委托任务执行状态推送，通常可以忽略该回调函数
```python
def on_taskstatus(task):
    print "on_taskstatus:"
    for key in task:    
        print "%20s : %s" % (key, str(task[key]))
```

设置回调函数
```python
tapi.set_ordstatus_callback(on_orderstatus)
tapi.set_trade_callback(on_trade)
tapi.set_task_callback(on_taskstatus)
```

### 算法交易

目前TradeSim提供TWAP和VWAP下单算法.

#### 以VWAP为例，样例代码如下：

```py
from jaqs.trade.tradeapi import TradeApi

# 登录仿真系统
tapi = TradeApi(addr="tcp://gw.quantos.org:8901") # tcp://gw.quantos.org:8901是仿真系统地址
user_info, msg = tapi.login("demo", "666666")     # 示例账户，用户需要改为自己注册的账户

# 选择策略号
tapi.use_strategy(123) # 123为给你分配的策略号，可以从user_info中获得

# VWAP算法参数
params = {
    "participate_rate": {"600000.SH": 0.5},
    "urgency":          {"600000.SH": 5},
    "price_range":      {"600000.SH": [16.5,17.1]},
    "lifetime":         5000,
    "min_unit_size":    {"600000.SH": 500}
}

# 下单接口，供支持三种下单风格

# Single Order Style
task_id, msg = tapi.place_order("600000.SH", "Buy", 17, 100, "vwap", params)
print("msg:", msg)
print("task_id:", task_id)

# Batch Order Style
orders = [
    {"security":"600030.SH", "action" : "Buy", "price": 16.10,  "size":1000},
    {"security":"600868.SH", "action" : "Buy", "price": 5.89,   "size":1000},
]

params = {
    "participate_rate": {"600030.SH": 0.5, "600868.SH": 0.5},
    "urgency":          {"600030.SH": 5, "600868.SH": 5},
    "lifetime":         5000
}

task_id, msg = tapi.place_batch_order(orders, "vwap", params)
print("msg:", msg)
print("task_id:", task_id)

# Basket Order Style
orders = [
    {"security":"600030.SH", "ref_price": 16.10,  "inc_size":1000},
    {"security":"600868.SH", "ref_price": 5.89,   "inc_size":-1000},
]

params = {
    "participate_rate": {"600030.SH": 0.5, "600868.SH": 0.5},
    "urgency":          {"600030.SH": 5, "600868.SH": 5},
    "lifetime":         5000,
}

task_id, msg = tapi.basket_order(orders, "vwap", params)
print("msg:", msg)
print("task_id:", task_id)
```

#### 以TWAP为例，样例代码如下：

```py
from tradeapi import TradeApi

# 登录仿真系统
tapi = TradeApi(addr="tcp://gw.quantos.org:8901") # tcp://gw.quantos.org:8901是仿真系统地址
user_info, msg = tapi.login("demo", "666666")     # 示例账户，用户需要改为自己注册的账户

# 选择策略号
tapi.use_strategy(123) # 123为给你分配的策略号，可以从user_info中获得

# 下单接口，供支持三种下单风格

# Single Order Style
params = {
    "urgency":          {"600868.SH": 5},
    "cycle":            1000,
    "max_unit_size":    {"600868.SH": 5},
    "lifetime":         5000，
    "price_range":      {"600868.SH": [5.8, 6.2]},
    "smart_speed":      [0.8,1.1,1.3]
}

task_id, msg = tapi.place_order("600868.SH", "Buy", 6.57, 100, "twap", params)
print("msg:", msg)
print("task_id:", task_id)

# Batch Order Style
orders = [
    {"security":"600030.SH", "action" : "Buy", "price": 16.10,  "size":1000},
    {"security":"600868.SH", "action" : "Buy", "price": 5.89,   "size":1000},
]

params = {
    "urgency":          {"600030.SH": 5, "600868.SH": 5},
    "cycle":            1000,
    "lifetime":         5000,
    "price_range_factor":0.1
}

task_id, msg = tapi.place_batch_order(orders, "twap", params)
print("msg:", msg)
print("task_id:", task_id)

```

### vnTrader的使用

vnTrader是一个可视化的下单工具，帮助用户下单和监控成交情况。

## 0. 软件下载。
+ 请首先安装[JAQS](https://github.com/quantOS-org/JAQS)，如已安装，请忽略。
+ 请从[这里](https://github.com/quantOS-org/TradeSim/tree/master/vnTrader)下载vnTrader, 如已下载，请忽略.

#### 1. 请在vnTrader程序目录，通过如下命令启动vnTrader:
```shell
python vtMain.py
```
在Windows上，也可以直接双击`start.bat`运行，如下图所示:

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_start.png)

#### 2. 系统提示登录，在登录框输入手机号和token，如下图

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_login.png)
**此时的策略号无法选择**，直接点击确定，系统会加载出策略号，如下图

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_strategy.png)

选择你要操作的策略号，再次点击确定，进入系统主界面，如下图：

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_main.png)

主界面主要包括：交易，行情，持仓，委托，成交，资金，日志，合约等几个大的面板，用于展示用户的详细交易信息。

*注：如想避免每次打开重复输入手机号和token，可在`vnTrader\setting\VT_setting.json`文件中修改`username`和`token`的值。*

#### 3. 发起委托

在交易界面，用户可以输入需要交易的标的代码、价格、数量，选择适当的算法，点击发单，即可进行委托。如下图

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_order.png)

#### 4. 发起撤单

有两种方式可以撤单：

1. 点击交易模块的“全撤”按钮。
2. 双击委托模块的指定委托记录。

![](https://github.com/quantOS-org/TradeSim/blob/master/doc/img/vnTrader_cancel.png)

### 仿真交易网页

+ 登录TradeSim网页，查看交易情况。访问地址是：[http://www.quantos.org/tradesim/trade.html](http://www.quantos.org/tradesim/trade.html)
+ 查看到自己的策略，当期的交易，持仓，绩效等情况

![](https://github.com/quantOS-org/quantOSUserGuide/blob/master/assets/tradesim_entrust.PNG?raw=true)

![](https://github.com/quantOS-org/quantOSUserGuide/blob/master/assets/tradesim_trade.PNG?raw=true)

![](https://github.com/quantOS-org/quantOSUserGuide/blob/master/assets/tradesim_pnl.PNG?raw=true)

+ 目前只有查询功能（实时、历史），未来会有更多丰富的分析功能、交易功能等
