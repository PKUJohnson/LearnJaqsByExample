# -*- coding:utf-8 -*-


"""
roe_yearly above 15%
roa_yearly above 5%

not new stock (listed before one year)

equal weight
universe : all sotcks
init_balance = 1e8

start_date 20130101
end_date   20171231

"""

import time

from jaqs.data import RemoteDataService
from jaqs.trade import AlphaBacktestInstance

import jaqs.util as jutil
import jaqs.trade.analyze as ana
from jaqs.trade import PortfolioManager
from jaqs.trade import AlphaStrategy
from jaqs.trade import AlphaTradeApi
from jaqs.trade import model
from jaqs.data import DataView

data_config = {
  "remote.data.address": "tcp://data.tushare.org:8910",
  "remote.data.username": "phone",
  "remote.data.password": "token"
}

trade_config = {
  "remote.trade.address": "tcp://gw.quantos.org:8901",
  "remote.trade.username": "phone",
  "remote.trade.password": "token"
}

dataview_folder = './data'
backtest_result_folder = './backtest'

start_date = 20160101
end_date   = 20171229

universe  = '000300.SH'
benchmark = '000300.SH'

def save_dataview():
    ds = RemoteDataService()
    ds.init_from_config(data_config)
    dv = DataView()
    
    props = {'start_date': start_date, 'end_date': end_date, 'universe': universe,
             'fields': 'roe_yearly,roa_yearly',
             'freq': 1}
    
    dv.init_from_config(props, ds)
    dv.prepare_data()
    
    dv.add_formula('roe_cond', 'roe_yearly >= 20', is_quarterly=True)
    dv.add_formula('roa_cond', 'roa_yearly >= 5', is_quarterly=True)
    dv.add_formula('cond', 'roe_cond && roa_cond', is_quarterly=True)
    
    dv.save_dataview(folder_path=dataview_folder)

def selector_roe_roa_not_new(context, user_options=None):
    snapshot = context.snapshot
    
    cond = snapshot['cond']
    
    df_inst = context.dataview.data_inst
    new_mask = context.trade_date - df_inst['list_date'] <= 10000
    new_stocks = new_mask.loc[new_mask].index
    cond.loc[new_stocks] = 0.0
    
    return cond

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


def backtest_analyze():
    ta = ana.AlphaAnalyzer()
    dv = DataView()
    dv.load_dataview(folder_path=dataview_folder)
    
    ta.initialize(dataview=dv, file_folder=backtest_result_folder)

    ta.do_analyze(result_dir=backtest_result_folder, selected_sec=list(ta.universe)[:3])


if __name__ == "__main__":
    t_start = time.time()
    
    save_dataview()
    alpha_strategy_backtest()
    backtest_analyze()
    
    t3 = time.time() - t_start
    print("\n\n\nTime lapsed in total: {:.1f}".format(t3))


