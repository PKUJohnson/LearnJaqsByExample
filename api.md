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

## 接口查询（help.apiList）
 
### 接口说明
 
查询quantos支持那些业务接口。
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 输入标志 | 说明 |
| --- | --- | --- | --- | --- |
| api | 参考数据接口 | String | N |  |
| name | 参考数据中文名 | String | N |  |
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 输出标志 | 说明 |
| --- | --- | --- | --- | --- |
| api | 参考数据接口 | String | Y |  |
| name | 参考数据中文名 | String | Y |  |
| comment | 注释 | String | Y |  |

### 接口说明备注(适用于所有接口)

+ Y : 必须输入或输出
+ N : 可选输入或输出，如果是输出参数，可以在fields里面指定。

## 接口参数查询（help.apiParam）
 
查询具体某个接口的输入和输出参数。
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 输入标志 | 说明 |
| --- | --- | --- | --- | --- |
| api | 参考数据接口 | String | N |  |
| ptype | 参数类型 | String | N | IN为输入参数，OUT为输出参数 |
| param | 参数代码 | String | N |  |
| must | 是否必要 | String | N | Y为必要参数，N为非必要参数 |
| pname | 参数中文名 | String | N |  |
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 输出标志 | 说明 |
| --- | --- | --- | --- | --- |
| api | 参考数据接口 | String | Y |  |
| param | 参数代码 | String | Y |  |
| ptype | 参数类型 | String | Y | IN为输入参数，OUT为输出参数 |
| dtype | 数据类型 | String | Y | String为字符串，Int为整型，Double为浮点型 |
| must | 是否必要 | String | Y | Y为必要参数，N为非必要参数 |
| pname | 参数中文名 | String | Y |  |
| comment | 注释 | String | Y |  |

## 分红送股（lb.secDividend）

查询股票的分红和送股信息。 
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 是否必输 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | 证券代码 | String | Y |  |
| start_date | 开始日期 | String | N | 除权除息日为筛选条件 |
| end_date | 结束日期 | String | N | 除权除息日为筛选条件 |
 
### 输入参数
 
| 字段 | 字段中文名 | 类型 | 是否必输 | 说明 |
| --- | --- | --- | --- | --- |
| symbol | 证券代码 | String | Y |  |
| div_enddate | 分红年度 | String | Y |  |
| ann_date | 预案公告日期 | String | Y |  |
| publish_date | 实施公告日期 | String | Y |  |
| record_date | 股权登记日 | String | Y |  |
| exdiv_date | 除权除息日 | String | Y |  |
| cash | 税前每股分红 | Double | Y |  |
| cash_tax | 税后每股分红 | Double | Y |  |
| share_ratio | 送股比例（每股） | Double | Y |  |
| share_trans_ratio | 转赠比例（每股） | Double | Y |  |
| cashpay_date | 派现日 | String | Y |  |
| bonus_list_date | 送股上市日 | String | Y |  |
 