# case 4：如何将JAQS对接实盘进行交易

社区很多朋友咨询，如何正确使用JAQS对接vnpy进行实盘交易，本文将完整介绍这一过程，解决大家的疑惑。

如果你想直接撸代码，请访问[这里](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/notebook/case4.zip)

## 1. 正确安装vnpy

vnpy目前最稳定的python环境是py2.7（32位），因此我们建议的安装方式是：

### 下载并安装anaconda。

下载地址：[Anaconda 5.0.1 for python2.7 32bit](https://www.anaconda.com/download/)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-1.png)

### 下载并安装vnpy。

**需要注意，不能使用pip安装，需要从github下载master分支的代码**

[下载地址](https://github.com/vnpy/vnpy)，注意选择master分支。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-2.png)

下载完成后，目录结构如下, 请在刚才安装的Anacanda，也就是“python2.7 32位”环境下，运行install.bat，安装vnpy。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-3.png)

## 2. 安装JAQS

请在刚才安装的Anacanda，也就是“python2.7 32位”环境下，执行两步：

+ 安装python-snappy，从[这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-snappys) 下载python-snappy的安装包。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-4.png)

```shell
pip install python_snappy-0.5.1-cp27-cp27m-win32.whl
```

+ 安装JAQS

```shell
pip install jaqs
```

## 3. 启动vnpy的JAQS服务

进入刚才下载的vnpy的代码目录，位于examples\VnTrader下，目录下的文件结构如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-5.png)

有三个重要的文件需要修改：

+ CTP_connect.json - CTP连接的信息
+ JS_setting.json - JAQS服务信息
+ run_jaqs.py - 启动JAQS的脚本

CTP_connect.json
```
{
    "brokerID": "9999", 
    "mdAddress": "tcp://180.168.146.187:10011", 
    "tdAddress": "tcp://180.168.146.187:10001", 
    "userID": "userID",
    "password": "password"    
}
```

JS_setting.json
```
{
    "host": "127.0.0.1",
    "port": 8901
}
```

+ JS_setting.json  配置JAQS的服务监听地址，一般不用修改。
+ CTP_connect.json 配置CTP服务器地址和账户信息，需要修改成你实盘的地址和账户信息。

run_jaqs.py
```python
def main():
    """主程序入口"""
    # 创建Qt应用对象
    qApp = createQApp()
    # 创建事件引擎
    ee = EventEngine()
    # 创建主引擎
    me = MainEngine(ee)
    # 添加交易接口
    me.addGateway(ctpGateway)
    # 添加上层应用
    me.addApp(jaqsService)
    
    # 创建主窗口
    mw = MainWindow(me, ee)
    mw.showMaximized()
    # 在主线程中启动Qt事件循环
    sys.exit(qApp.exec_())

if __name__ == '__main__':
    main()
```

run_jaqs.py是一个主程序，在这个主程序里面，添加了ctpGateway和jaqsService两个模块。

ctpGateway是真正的实盘交易通道，jaqsService是服务转接模块。

启动方法很简单，运行 python run_jaqs.py 即可！

运行成功，则会出现vnpy经典的主界面，如下图所示：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-6.png)

在“功能”菜单，会出现一个“Jaqs服务”，点击之后，是一个消息文本框，用于查看jaqs服务的运行日志。

这是表明，JAQS的服务已经启动成功了。

## 4. 启动CTP交易通道

这个和vnpy启动其他交易通道的方法完全相同，在系统菜单下，点击“连接CTP”即可。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-7.png)

运行成功的界面如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-8.png)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-9.png)

## 5. 启动JAQS策略，对接vnpy

这里我们举一个特别简单的策略的例子，来说明一下JAQS策略如何进行实盘。策略原理：

+ (1) 做rb1805.SHF和rb1810.SHF的价差套利，如果价差超过195，则空rb1805.SHF，多rb1810.SHF，如果价差小于180，则反向做。
+ (2) 为了演示效果，只开仓不平仓。
+ (3) 策略启动后，根据tick数据，实时计算价差。
+ (4) 每次策略启动只做一次来回。

参考代码如下：
```python
data_config = {
  "remote.data.address": "tcp://data.tushare.org:8910",
  "remote.data.username": "phone",
  "remote.data.password": "token"
}

trade_config = {
  "remote.trade.address": "tcp://127.0.0.1:8901",
  "remote.trade.username": "username",
  "remote.trade.password": "password"
}

def run_strategy():
    tapi = RealTimeTradeApi(trade_config, prod_type = "jaqs")
    ins = EventLiveTradeInstance()
    
    ds    = RemoteDataService()
    strat = SpreadAlgo()
    pm    = PortfolioManager()
    
    props = {
        "symbol"       : "rb1805.SHF,rb1810.SHF",
        "tick_sizes"   : [1.0, 1.0],
        "open_spread"  : 195,
        "close_spread" : 180
    }
    
    props.update(data_config)
    props.update(trade_config)
    
    context = model.Context(data_api=ds, trade_api=tapi,
                              instance=ins, strategy=strat, pm=pm)
    
    ins.init_from_config(props)
    
    ds.subscribe(props['symbol'])
    
    ins.run()


if __name__ == "__main__":
    run_strategy()

```

只要将交易发送的地址，修改成“tcp://127.0.0.1:8901”，这个地址就是之前vnpy启动本地Jaqs服务的地址。

SpreadAlgo策略代码不在文章中贴出，请大家直接下载代码。

运行后，策略会根据条件，选择是否开仓，在vnpy的界面，可以看到开仓结果。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/case4-10.png)

是不是很简单？

## 6. 想尝试一下？

请访问www.quantos.org，下载安装JAQS，开始自己的量化旅程吧。

这里的东西都是开源和免费的。
