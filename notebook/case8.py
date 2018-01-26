# -*- coding:utf-8 -*-

import time

import numpy as np

from jaqs.data import RemoteDataService
from jaqs.data.basic import Bar, Quote
from jaqs.trade import (model, EventLiveTradeInstance, EventBacktestInstance, RealTimeTradeApi,
                        EventDrivenStrategy, BacktestTradeApi, PortfolioManager, common)
import jaqs.trade.analyze as ana
import jaqs.util as jutil

data_config = {
  "remote.data.address": "tcp://10.2.0.14:8910",
  "remote.data.username": "xxx",
  "remote.data.password": "xxx"
}
trade_config = {
  "remote.trade.address": "tcp://gw.quantos.org:8901",
  "remote.trade.username": "xxx",
  "remote.trade.password": "xxx"
}

result_dir_path = './double_ma'

class DoubleMaStrategy(EventDrivenStrategy):
    """"""
    def __init__(self):
        super(DoubleMaStrategy, self).__init__()

        # 标的
        self.symbol = ''

        # 快线和慢线周期
        self.fast_ma_len = 0
        self.slow_ma_len = 0
        
        # 记录当前已经过的天数
        self.window_count = 0
        self.window = 0

        # 快线和慢线均值
        self.fast_ma = 0
        self.slow_ma = 0
        
        # 固定长度的价格序列
        self.price_arr = None

        # 当前仓位
        self.pos = 0

        # 下单量乘数
        self.buy_size_unit = 1
        self.output = True
    
    def init_from_config(self, props):
        """
                        将props中的用户设置读入
        """
        super(DoubleMaStrategy, self).init_from_config(props)
        # 标的
        self.symbol = props.get('symbol')

        # 初始资金
        self.init_balance = props.get('init_balance')

        # 快线和慢线均值
        self.fast_ma_len = props.get('fast_ma_length')
        self.slow_ma_len = props.get('slow_ma_length')
        self.window = self.slow_ma_len + 1
        
        # 固定长度的价格序列
        self.price_arr = np.zeros(self.window)

    def buy(self, quote, size=1):
        """
                        这里传入的'quote'可以是:
            - Quote类型 (在实盘/仿真交易和tick级回测中，为tick数据)
            - Bar类型 (在bar回测中，为分钟或日数据)
                        我们通过isinsance()函数判断quote是Quote类型还是Bar类型
        """
        if isinstance(quote, Quote):
            # 如果是Quote类型，ref_price为bidprice和askprice的均值
            ref_price = (quote.bidprice1 + quote.askprice1) / 2.0
        else:
            # 否则为bar类型，ref_price为bar的收盘价
            ref_price = quote.close
            
        task_id, msg = self.ctx.trade_api.place_order(quote.symbol, common.ORDER_ACTION.BUY, ref_price, self.buy_size_unit * size)

        if (task_id is None) or (task_id == 0):
            print("place_order FAILED! msg = {}".format(msg))
    
    def sell(self, quote, size=1):
        if isinstance(quote, Quote):
            ref_price = (quote.bidprice1 + quote.askprice1) / 2.0
        else:
            ref_price = quote.close
    
        task_id, msg = self.ctx.trade_api.place_order(quote.symbol, common.ORDER_ACTION.SHORT, ref_price, self.buy_size_unit * size)

        if (task_id is None) or (task_id == 0):
            print("place_order FAILED! msg = {}".format(msg))
    
    def on_bar(self, quote_dic):
        """
                        这里传入的'quote'可以是:
            - Quote类型 (在实盘/仿真交易和tick级回测中，为tick数据)
            - Bar类型 (在bar回测中，为分钟或日数据)
                        我们通过isinsance()函数判断quote是Quote类型还是Bar类型
        """
        quote = quote_dic.get(self.symbol)
        if isinstance(quote, Quote):
            # 如果是Quote类型，mid为bidprice和askprice的均值
            bid, ask = quote.bidprice1, quote.askprice1
            if bid > 0 and ask > 0:
                mid = (quote.bidprice1 + quote.askprice1) / 2.0
            else:
                # 如果当前价格达到涨停板或跌停板，系统不交易
                return
        else:
            # 如果是Bar类型，mid为Bar的close
            mid = quote.close

        # 将price_arr序列中的第一个值删除，并将当前mid放入序列末尾
        self.price_arr[0: self.window - 1] = self.price_arr[1: self.window]
        self.price_arr[-1] = mid
        self.window_count += 1

        if self.window_count <= self.window:
            return

        # 计算当前的快线/慢线均值
        self.fast_ma = np.mean(self.price_arr[-self.fast_ma_len:])
        self.slow_ma = np.mean(self.price_arr[-self.slow_ma_len:])

        print(quote)
        print("Fast MA = {:.2f}     Slow MA = {:.2f}".format(self.fast_ma, self.slow_ma))

        # 交易逻辑：当快线向上穿越慢线且当前没有持仓，则买入100股；当快线向下穿越慢线且当前有持仓，则平仓
        if self.fast_ma > self.slow_ma:
            if self.pos == 0:
                self.buy(quote, 10000)

        elif self.fast_ma < self.slow_ma:
            if self.pos > 0:
                self.sell(quote, self.pos)

    def on_trade(self, ind):
        """
                        交易完成后通过self.ctx.pm.get_pos得到最新仓位并更新self.pos
        """
        print("\nStrategy on trade: ")
        print(ind)
        self.pos = self.ctx.pm.get_pos(self.symbol)


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

    tapi = BacktestTradeApi()
    ins = EventBacktestInstance()
        
    props.update(data_config)
    props.update(trade_config)
    
    ds = RemoteDataService()
    strat = DoubleMaStrategy()
    pm = PortfolioManager()
    
    context = model.Context(data_api=ds, trade_api=tapi, instance=ins,
                            strategy=strat, pm=pm)
    
    ins.init_from_config(props)

    ins.run()

    ins.save_results(folder_path=result_dir_path)


def analyze():
    ta = ana.EventAnalyzer()
    
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    
    ta.initialize(data_server_=ds, file_folder=result_dir_path)
    
    ta.do_analyze(result_dir=result_dir_path, selected_sec=[])


if __name__ == "__main__":
    run_strategy()
    analyze()