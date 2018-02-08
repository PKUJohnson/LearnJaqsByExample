# 基础数据

## 调用说明
- 通过api.query函数调用，第一个参数view需填入对应的接口名，如：`view="jz.instrumentInfo"` 
- 输入参数指的是filter参数里面的内容，通过'&'符号拼接，如：`filter="inst_type=&status=1&symbol="` 
- 输出参数指的是fields里面的内容，通过','隔开

样例代码：获取上市股票列表
```python
df, msg = api.query(
                view="jz.instrumentInfo", 
                fields="status,list_date, fullname_en, market", 
                filter="inst_type=1&status=1&symbol=", 
                data_format='pandas')
```

## 目前支持的接口及其含义

| 接口               | view                  | 分类       |
| ------------------ | --------------------- | ---------- |
| 证券基础信息表     | jz.instrumentInfo     | 基础信息   |
| 交易日历表         | jz.secTradeCal        | 基础信息   |
| 分配除权信息表     | lb.secDividend        | 股票       |
| 复权因子表         | lb.secAdjFactor       | 股票       |
| 停复牌信息表       | lb.secSusp            | 股票       |
| 行业分类表         | lb.secIndustry        | 股票       |
| 指数基本信息表     | lb.indexInfo          | 指数       |
| 指数成份股表       | lb.indexCons          | 指数       |
| 公募基金净值表     | lb.mfNav              | 基金       |

## 分红送股（lb.secDividend）
 
### 接口说明
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 说明 |
| --- | --- | --- | --- |
| symbol | 证券代码 | String |  |
| start_date | 开始日期 | String | 除权除息日为筛选条件 |
| end_date | 结束日期 | String | 除权除息日为筛选条件 |
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 说明 |
| --- | --- | --- | --- |
| symbol | 证券代码 | String |  |
| div_enddate | 分红年度 | String |  |
| ann_date | 预案公告日期 | String |  |
| publish_date | 实施公告日期 | String |  |
| record_date | 股权登记日 | String |  |
| exdiv_date | 除权除息日 | String |  |
| cash | 税前每股分红 | Double |  |
| cash_tax | 税后每股分红 | Double |  |
| share_ratio | 送股比例（每股） | Double |  |
| share_trans_ratio | 转赠比例（每股） | Double |  |
| cashpay_date | 派现日 | String |  |
| bonus_list_date | 送股上市日 | String |  |
 
### 使用示例
 
```python

```
