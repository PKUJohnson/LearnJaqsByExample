# encoding: UTF-8

import urllib
import requests
import hashlib
import hmac
import base64
import json
from datetime import datetime
from collections import OrderedDict
import pandas as pd

class HuobiAgent:
    '''
    symbol: btcusdt, bchbtc
    period: 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    '''
    
    def __init__(self):
        self.AccessKeyId = 'b720f47b-8acefaa6-fdd41817-a6dd7'
        self.PrivateKey  = 'b78240de-03ade0eb-07c00462-cabe0'

        self.SignatureMethod  = 'HmacSHA256'
        self.SignatureVersion = 2
        self.BaseUrl          = 'https://api.huobipro.com'

    # do rest request 
    def do_request(self, api, param):
        # prepare request data
        URL  = self.BaseUrl + api

        # request header
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/57.0.2987.133 Safari/537.36 "
    
        # simulate http request
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Content-Type'] = 'application/json'

        res = session.get(URL, params=param)
        if res.status_code != 200:
            print("query_error, status_code = ", res.status_code)
            return None, res.status_code

        # return http response
        rsp = res.text
        return rsp, ''
    
    def make_param(self, req_api, req_dict):
        param = OrderedDict()
        param['AccessKeyId']      = self.AccessKeyId
        param['SignatureMethod']  = self.SignatureMethod
        param['SignatureVersion'] = self.SignatureVersion
        param.update(req_dict)

        param_encode = urllib.parse.urlencode(param)

        # message for digital signature
        '''
        GET\n
        api.huobi.pro\n
        api\n
        '''
        method = 'GET\n'
        url    = 'api.huobi.pro\n'
        api    = req_api + '\n' 

        message = method + url + api + param_encode

        # make signature by hashlib and hmac
        hmac_value = hmac.new(self.PrivateKey.encode(), message.encode(), digestmod=hashlib.sha256).digest();
        signature = base64.encodebytes(hmac_value)
        param['Signature'] = signature
        
        return param
    
    # get realtime market quote
    def get_quote(self, symbol):
        
        req_api  = '/market/detail/merged'
        req_dict = {'symbol' : symbol} 
        param = self.make_param(req_api, req_dict)
        
        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        # 载入数据并记录
        rsp_json = json.loads(response)
        
        status = rsp_json['status']
        if status != 'ok':
            msg = rsp_json['err-code'] + ":" + rsp_json['err-msg']   
            return None, msg
        
        raw_records = rsp_json['tick']
        raw_records['askprice'] = raw_records['ask'][0]
        raw_records['askvolume'] = raw_records['ask'][1]
        
        raw_records['bidprice'] = raw_records['bid'][0]
        raw_records['bidvolume'] = raw_records['bid'][1]
        
        raw_records.pop('ask')
        raw_records.pop('bid')
        
        df = pd.DataFrame().from_dict(raw_records, orient='index').T

        return df, ''

    def get_kline(self, symbol, period, size):
        
        req_api  = '/market/history/kline'
        req_dict = {
            'symbol' : symbol,
            'period' : period,
            'size'   : size
        } 
        param = self.make_param(req_api, req_dict)
        
        response, msg = self.do_request(req_api, param)
        
        if response is None:
            return None, msg
        
        # 载入数据并记录
        rsp_json = json.loads(response)
        
        status = rsp_json['status']
        if status != 'ok':
            msg = rsp_json['err-code'] + ":" + rsp_json['err-msg']
            return None, msg
        
        raw_records = rsp_json['data']
        
        df = pd.DataFrame().from_dict(raw_records)
        
        df['time'] = df['id'].apply(lambda x: datetime.fromtimestamp(x))
        df.set_index('time', inplace=True)
        df.sort_index(ascending=True, inplace=True)
        
        return df, ''

    def get_market_depth(self, symbol, dep_type):
        '''
        type: step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
        '''
        req_api  = '/market/depth'
        req_dict = {
            'symbol' : symbol,
            'type' : dep_type        
        } 
        param = self.make_param(req_api, req_dict)
        
        response = self.do_request(req_api, param)
        return response
    
    def get_trade(self, symbol):
        req_api  = '/market/trade'
        req_dict = {
            'symbol' : symbol        
        } 
        param = self.make_param(req_api, req_dict)
        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        # 载入数据并记录
        rsp_json = json.loads(response)
        
        status = rsp_json['status']
        if status != 'ok':
            msg = rsp_json['err-code'] + ":" + rsp_json['err-msg']
            return None, msg
        
        raw_records = rsp_json['tick']['data']
        data_records = []
        for record in raw_records:
            record['id'] = str(record['id'])
            data_records.append(record)
        
        df = pd.DataFrame().from_dict(data_records)
        df['time'] = df['ts'].apply(lambda x: datetime.fromtimestamp(x/1000))
        
        return df,''
    
    def get_hist_trade(self, symbol, size=2000):
        req_api  = '/market/history/trade'
        req_dict = {
            'symbol' : symbol,
            'size'   : size
        } 
        param = self.make_param(req_api, req_dict)
        response, msg = self.do_request(req_api, param)
        if response is None:
            return None, msg
        
        # 载入数据并记录
        rsp_json = json.loads(response)
        
        status = rsp_json['status']
        if status != 'ok':
            msg = rsp_json['err-code'] + ":" + rsp_json['err-msg']
            return None, msg
        
        raw_records = rsp_json['data']
        data_records = []
        for record in raw_records:
            elems = record['data']
            for elem in elems:
                elem['id'] = str(elem['id'])
                data_records.append(elem)
        
        df = pd.DataFrame().from_dict(data_records)
        df['time'] = df['ts'].apply(lambda x: datetime.fromtimestamp(x/1000))
        df.set_index('time', inplace=True)
        df.sort_index(ascending=True, inplace=True)
        
        return df,''
