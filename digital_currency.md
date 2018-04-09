# 数字货币量化交易基础（2）

在上篇文章里，我简单介绍了一下如何获取火币网的数字货币行情，得到了很多的读者反馈：

+ 火币在国内被封了，无法访问
+ 太简单了，没有更加深入的介绍数字货币的量化交易

为了响应大家的要求，我趁着假期严肃的研究了一下，先将相关的研究成果分享出来。

本文包括如下几个部分：

+ 我应该关注那些数字货币？
+ 为什么需要数字货币交易所？
+ 数字货币的交易所是怎么运作的？
+ 如何选择交易所？
+ 如何进行数字货币的程序化交易？
+ 有哪些量化交易策略可以使用？

## 我应该关注哪些数字货币？

这个问题其实非常简单，只需要关注目前最主流的几个就行。

1. 比特币（BTC）
2. 莱特币（LTC）
3. 以太币（ETH）
4. 比特币现金（BCH）
5. 瑞波币（XPR）

## 为什么需要数字货币交易所？

这是一个非常好的问题。数字货币的重大创新中，最核心的一条就是去中心化。即数字货币的运行，不需要一个中心化的组织来管理。

但为了达到去中心化的目的，数字货币也必须要付出一定的代价。这个代价包括：

1、转账确认的速度慢

+ 比特币的安全确认时间大约是1小时
+ 莱特币的安全确认时间大约是10-15分钟
+ 以太币的安全确认时间大约是5-10分钟

这样的速度是没有办法满足很多用户需求的。

2、对用户使用的要求高

要能安全的使用数字货币进行支付和转账，你需要了解好多好多的概念，比如钱包地址、区块、确认、分叉等。
这些都增加了普通用户使用数字货币的复杂度。

数字货币交易所可以部分的解决这些问题，后面我细细讲解。

## 数字货币的交易所是怎么运作的？

数字货币交易所是一个完全中心化运作的组织，方便用户进行数字货币的交易，是一个交易中介。

交易所提供的服务主要包括：

1. 资产的管理，包括账户管理，账户下面的资金及数字货币资产管理。
2. 交易服务，包括订单的管理、交易撮合、交易的结算等。
3. 资讯服务，包括提供市场的行情、成交信息、订单队列等。

有一些交易所还会提供一些增值的服务，比如数字货币的期货交易，杠杆交易，融资或融币的交易。

交易所提供的交易品种包括：

1、法币与数字货币之间的交易，如：
+ BTC-USD，比特币与美元间的交易
+ BTC-EUR，比特币与欧元间的交易

2、数字货币之间的交易，如：
+ BTC-BCH，比特币与比特币现金之间的交易
+ BTC-LTC，比特币与莱特币之间的交易

对于一个普通用户而言，交易所会为用户创建一个虚拟账户，用户可以

1. 把资金从银行转账到交易所账户，简称充值。或者将资金从交易所账户转账到银行，简称提现。
2. 将数字货币从钱包转账到交易所账户，简称充币。或者将数字货币从交易所账户转账到钱包，简称提币。
3. 在交易所内部，使用交易所账户买卖数字货币。

为什么很多国家要加强对数字货币交易所的监管呢？
道理非常简单，你往交易所转入的都是真金白银，交易所只是给你开了个虚拟账户。交易所全凭着自己的信誉来获得你的信任。
如果交易所突然跑路了，网站打不开了，你的资金和数字货币资产可就都没有了。

在中国为了防范金融风险，直接取缔了所有私营的数字货币交易所，也是非常合理的。

## 如何选择交易所？

我的选择标准是，选择主流的、交易量大的、流动性好的交易所。

由于国内的交易所已经全部取缔了，因此你只能使用境外交易所提供的服务。推荐几个：

1. Bitfinex（www.bitfinex.com）
2. Bitstamp（www.bitstamp.net）
3. Bittrex（www.bittrex.com）
4. GDAX（www.gdax.com）
5. OKCoin（www.OKCoin.com）

## 如何进行数字货币的程序化交易？

数字货币的交易和股票很类似，交易所也提供非常丰富的市场信息，包括行情、成交信息、订单簿等等。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/bittrex.png)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/bitstamp.png)

交易所同时提供API接入，可以直接进行程序化交易。（目前国内的股票交易是禁止API接入的）

我简单梳理了一下，交易所目前都提供两种类型的API接口：

1. REST风格的API，用于查询市场数据、账户信息和提交交易订单。
2. WebSocket风格的API，用于推送实时的市场数据、成交信息。

推送接口主要包括：
+ 实时行情ticker
+ 实时订单队列orderbook（eg. top 100bids/asks）
+ 实时订单信息orders

Rest查询和交易接口包括：
+ 实时行情ticker
+ 实时订单队列orderbook
+ 实时成交信息transaction
+ 历史K线信息history candlstick
+ 可交易标的信息symbols
+ 账户余额信息account balance
+ 订单请求BUY/SELL Limit/Market Order
+ 撤销订单Cancel Order
+ 查询订单状态Query Order Status
+ 充值提现WithDraw/Deposit

在接口使用上，建议：
+ 用户可以根据自己的业务场景，使用不同的API，也可以组合起来使用。
+ 各个交易所都会提供python接口，对一般的程序化交易用户，应该能满足要求。如果对性能要求特别高，也可以自己用高级语言写。
+ 如果访问的不是市场数据，需要使用数字签名。交易所会给用户生成相应的API Key，用户要保管好Key。

如果使用python接口，github上有一个开源的项目[bitex](https://github.com/Crypto-toolbox/bitex)，对通信做了比较好的封装。

## 有哪些量化交易策略可以使用？

数字货币的交易是一个很新的东西，具体哪些量化策略可以使用，我觉得是一个见仁见智的问题。

作者猜测：

1. 传统基于统计的量化策略，由于历史数据的时间太短，不好进行回测，只能实盘边跑边修正。
2. 目前应该还是数字货币交易的早期，比较高频的策略应该会有好的效果。
3. 由于信息的不对称、流动性等问题，一些无风险的套利策略，看看有没有有机会。

光说不练假把式，不动手的量化都是耍流氓。下面我们就练一下，看看那些套利策略可能有机会。

### 策略准备，开发获取交易所实时行情的接口(REST接口)

```python
import urllib
import requests
import hashlib
import hmac
import base64
import json
import datetime
from collections import OrderedDict
import pandas as pd

'''
symbol: 
数字货币美元：btcusd, bchusd, ltcusd, ethusd
数字货币欧元：btceur, bcheur, ltceur, etheur
币币交易：bchbtc
汇率交易：eurusd
'''
class Quote():
    def __init__(self):
        self.askprice  = 0.0
        self.askvolume = 0.0
        self.bidprice  = 0.0
        self.bidvolume = 0.0
        self.open      = 0.0
        self.high      = 0.0
        self.low       = 0.0
        self.close     = 0.0
        self.vol       = 0.0
        self.amount    = 0.0
        self.symbol    = ''
        self.exchange  = ''
        self.time      = ''

    def to_string(self):
        print('ask : %.6f %.8f' % (self.askprice, self.askvolume))
        print('bid : %.6f %.8f' % (self.bidprice, self.bidvolume))
        print('open: %.6f high : %.6f' % (self.open, self.high))
        print('low : %.6f close: %.6f' % (self.low, self.close))
        print('vol : %.6f amount: %.6f'% (self.vol, self.amount))
        print(self.time)
        print(self.symbol, self.exchange)
        
class BaseAgent:
    
    def __init__(self):
        self.BaseUrl = ''
    
    # do rest request 
    def do_request(self, api, param):
        # prepare request data
        URL  = self.BaseUrl + api

        # request header
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/57.0.2987.133 Safari/537.36 "
    
        proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }       
        
        # simulate http request
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        res = session.get(URL, params=param, proxies=proxies)
        if res.status_code != 200:
            print("query_error, status_code = ", res.status_code)
            return None, res.status_code

        # return http response
        rsp = res.text
        return rsp, ''

    def make_param(self, req_api, req_dict):
        param = OrderedDict()
        param.update(req_dict)

        return param

    '''
    get realtime market quote return df, msg
    '''
    def get_quote(self, symbol):
        pass

class OKCoinAgent(BaseAgent):

    def __init__(self):
        self.BaseUrl          = 'https://www.okcoin.com'
        
        self.SymbolMap = {
            'btcusd' : 'btc_usd',
            'bchusd' : 'bch_usd',
            'ltcusd' : 'ltc_usd',
            'ethusd' : 'eth_usd'
        }
        
    # get realtime market quote
    def get_quote(self, symbol):
        
        req_api  = '/api/v1/ticker.do'
        req_dict = {'symbol' : self.SymbolMap[symbol]} 
        param = self.make_param(req_api, req_dict)
        
        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        # 载入数据并记录
        rsp_json = json.loads(response)
        
        if 'error_code' in rsp_json:
            msg = rsp_json['error_code']
            return None, msg
        
        time = float(rsp_json['date'])
        raw_records = rsp_json['ticker']
        dt = datetime.datetime.fromtimestamp(time)

        quote = Quote()
        quote.time = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

        quote.askprice = float(raw_records['sell'])
        quote.bidprice = float(raw_records['buy'])
        quote.close    = float(raw_records['last'])
        quote.vol      = float(raw_records['vol'])
        quote.high     = float(raw_records['high'])
        quote.low      = float(raw_records['low'])
        
        quote.symbol   = symbol
        quote.exchange = 'OKCoin'
        
        return quote, ''
		
class CoinBaseAgent(BaseAgent):

    def __init__(self):
        self.BaseUrl          = 'https://api.gdax.com'
        
        self.SymbolMap = {
            'btcusd' : 'BTC-USD',
            'btceur' : 'BTC-EUR',
            'bchusd' : 'BCH-USD',
            'bcheur' : 'BCH-EUR',
            'ltcusd' : 'LTC-USD',
            'ltceur' : 'LTC-EUR',
            'ethusd' : 'ETH-USD',
            'etheur' : 'ETH-EUR'
        }

    # get realtime market quote
    def get_quote(self, symbol):
        
        req_api  = '/products/%s/ticker' % self.SymbolMap[symbol]
        req_dict = {} 
        param = self.make_param(req_api, req_dict)
        
        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        raw_records = json.loads(response)
        
        utcTime = datetime.datetime.strptime(raw_records['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        localtime = utcTime + datetime.timedelta(hours=8)
        
        quote = Quote()
        quote.time = datetime.datetime.strftime(localtime, '%Y-%m-%d %H:%M:%S')

        quote.askprice = float(raw_records['ask'])
        quote.bidprice = float(raw_records['bid'])
        quote.close    = float(raw_records['price'])
        quote.vol      = float(raw_records['size'])
        quote.amount   = float(raw_records['volume'])
        
        quote.symbol   = symbol
        quote.exchange = 'CoinbaseGDAX'

        return quote, ''

class BitstampAgent(BaseAgent):

    def __init__(self):
        self.BaseUrl          = 'https://www.bitstamp.net'
        
    # get realtime market quote
    def get_quote(self, symbol):
        
        req_api  = '/api/v2/ticker/%s' % symbol
        req_dict = {} 
        param = self.make_param(req_api, req_dict)

        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        raw_records = json.loads(response)
        
        localtime = datetime.datetime.fromtimestamp(int(raw_records['timestamp']))
        
        quote = Quote()
        quote.time = datetime.datetime.strftime(localtime, '%Y-%m-%d %H:%M:%S')

        quote.open     = float(raw_records['open'])
        quote.high     = float(raw_records['high'])
        quote.low      = float(raw_records['low'])
        quote.askprice = float(raw_records['ask'])
        quote.bidprice = float(raw_records['bid'])
        quote.close    = float(raw_records['last'])
        quote.vol      = float(raw_records['volume'])
        
        quote.symbol   = symbol
        quote.exchange = 'Bitstamp'

        return quote, ''		
```

### 套利策略1：跨交易所间的套利

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/coin_arb_1.png)

思路非常简单，交易所之间交易相同的比特币，但价格有比较明显的差距，就可以在交易所之间套利。

1. 在交易所A低价买入数字货币
2. 在交易所A提取数字货币
3. 将数字货币存入交易所B
4. 将数字货币在交易所B高价卖出
5. 在交易所B提取资金

这个策略的问题在于：
1. 交易所提币的时间很长，一般超过1个小时，存在时间上的风险
2. 提币和提取资金都需要手续费，有些交易所是按照每次收费的，所以金额和数量太小，费用占比会很高。

所以这个策略的改进版是：
1. 用户手里持有一些数字货币，存入交易所B
2. 每在交易所B高价卖出一些数字货币后，在交易所A低价买入等量的数字货币。
3. 交易所B里面的币卖光后，再把交易所A里面的币提取出来，转入交易所B。

这个方法规避了时间风险和手续费的问题，但引入了一个更大的风险:数字货币的持仓风险。

我们来看一看各个交易所的情况：
```python
agent = OKCoinAgent()
quote, msg = agent.get_quote('btcusd')
quote.to_string()

agent = CoinBaseAgent()
quote, msg = agent.get_quote('btcusd')
quote.to_string()

agent = BitstampAgent()
quote, msg = agent.get_quote('btcusd')
quote.to_string()
```
output:
```html
ask : 7498.880000 0.00000000
bid : 7342.810000 0.00000000
open: 0.000000 high : 7950.240000
low : 7382.010000 close: 7499.850000
vol : 92.590000 amount: 0.000000
2018-04-09 18:56:07
btcusd OKCoin

ask : 6794.050000 0.00000000
bid : 6794.040000 0.00000000
open: 0.000000 high : 0.000000
low : 0.000000 close: 6793.500000
vol : 0.219400 amount: 9875.275370
2018-04-09 18:55:59
btcusd CoinbaseGDAX

ask : 6796.660000 0.00000000
bid : 6793.220000 0.00000000
open: 7027.260000 high : 7175.830000
low : 6760.000000 close: 6793.220000
vol : 7082.738112 amount: 0.000000
2018-04-09 18:56:08
btcusd Bitstamp
```

不难发现：
+ OKCoin上比特币美元的价格比Bitstamp和CoinbaseGDAX都要贵500多美元，因此理论上存在跨交易所套利的可能。
+ Bitstamp和CoinbaseGDAX上的价格就非常接近，不存在套利空间。

为什么OKCoin上会有这么大的差异呢？仔细看很容易发现，OKCoin上的交易量很小，只有其他交易所的百分之一。
因此我判断可能的原因是：
1. OKCoin是中国人开的交易所，欧美用户参与不多。
2. OKCoin的量太小，即使套利也没有多少量，但交易所关门的风险很大，所以也就没有大的玩家参与套利。

### 套利策略2：利用价差和汇率进行套利

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/coin_arb_2.png)

套利涉及三个品种，步骤如下：
1. 先用美元买入比特币BTC-USD
2. 再将比特币用欧元卖出BTC-EUR
3. 最后将欧元兑换成美元EUR-USD

这个过程涉及三次买卖，因此也需要考虑手续费和交易的冲击成本。

这个策略要想成立，就需要满足 P(BTC-USD) < P(BTC-EUR) * P(EUR-USD) - 手续费

我们可以简单看一下Bitstamp上这三者的关系：
```python
agent = BitstampAgent()
quote, msg = agent.get_quote('btcusd')
quote.to_string()

agent = BitstampAgent()
quote, msg = agent.get_quote('btceur')
quote.to_string()

agent = BitstampAgent()
quote, msg = agent.get_quote('eurusd')
quote.to_string()
```

output: 
```html
ask : 6765.120000 0.00000000
bid : 6759.140000 0.00000000
open: 7027.260000 high : 7175.830000
low : 6708.010000 close: 6759.140000
vol : 7413.376477 amount: 0.000000
2018-04-09 19:07:46
btcusd Bitstamp
ask : 5524.860000 0.00000000
bid : 5517.900000 0.00000000
open: 5728.500000 high : 5842.000000
low : 5465.000000 close: 5519.430000
vol : 1296.930089 amount: 0.000000
2018-04-09 19:07:45
btceur Bitstamp
ask : 1.228490 0.00000000
bid : 1.225120 0.00000000
open: 1.226150 high : 1.230660
low : 1.225000 close: 1.228490
vol : 368447.295920 amount: 0.000000
2018-04-09 19:07:47
eurusd Bitstamp
```

result:
+ P(BTC-USD) = 6765.12
+ P(BTC-EUR) * P(EUR-USD) = 5517.90 * 1.225120 = 6760.08

这个时候，已经没有套利空间了。

### 套利策略3：利用币币交易进行套利

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/coin_arb_3.png)

套利涉及三个品种，步骤如下：
1. 先用美元买入比特币(BTC-USD)
2. 再通过币币交易将比特币换成BCH(BCH-BTC)
3. 最后将BCH卖出成美元BCH-USD

这个过程涉及三次买卖，因此也需要考虑手续费和交易的冲击成本。

这个策略要想成立，就需要满足 P(BTC-USD) < 1 / P(BCH-BTC) * P(BCH-USD) - 手续费

我们可以简单看一下Bitstamp上这三者的关系：
```python
agent = BitstampAgent()
quote, msg = agent.get_quote('btcusd')
quote.to_string()

agent = BitstampAgent()
quote, msg = agent.get_quote('bchbtc')
quote.to_string()

agent = BitstampAgent()
quote, msg = agent.get_quote('bchusd')
quote.to_string()

```

output:
```html
ask : 6755.120000 0.00000000
bid : 6755.110000 0.00000000
open: 7027.260000 high : 7175.830000
low : 6708.010000 close: 6750.160000
vol : 7507.565418 amount: 0.000000
2018-04-09 19:15:54
btcusd Bitstamp

ask : 0.094685 0.00000000
bid : 0.094287 0.00000000
open: 0.093190 high : 0.095580
low : 0.092340 close: 0.094315
vol : 272.738682 amount: 0.000000
2018-04-09 19:15:54

bchbtc Bitstamp
ask : 638.210000 0.00000000
bid : 636.150000 0.00000000
open: 653.830000 high : 680.000000
low : 633.590000 close: 638.430000
vol : 1458.992858 amount: 0.000000
2018-04-09 19:15:56
bchusd Bitstamp
```
result:
+ P(BTC-USD) = 6755.12
+ 1 / P(BCH-BTC) * P(BCH-USD) = 1 / 0.094685 * 636.15 = 6718.60

这种方式也没有套利机会

看来在Bitstamp上，比特币交易的流动性足够好，已经没有这种简单的公式套利的机会了。

至于其他更加复杂的交易策略，就需要读者你自己去摸索。

总之：炒币有风险，投资需谨慎。预祝大家好运！
