# 开源爬虫工具OpenDataTools及其使用样例

## 项目介绍

+ OpenDataTools是一个开源爬虫工具,通过爬虫将各种数据接口简化,方便用户使用. 由QuantOS团队开发. 
+ 目前的版本是:0.0.7
+ 目前只支持 空气质量AQI 的数据获取.
+ 项目地址: https://github.com/PKUJohnson/OpenData, 感兴趣的同学可以去研究代码.

## 样例介绍

空气质量数据AQI, 数据来源于 环保部网站. http://datacenter.mep.gov.cn/

## 准备工作

安装opendatatools(开源的数据爬虫工具)
+ pip install opendatatools 

安装pyecharts 
+ pip install pyecharts
+ pip install echarts-countries-pypkg  
+ pip install echarts-china-provinces-pypkg  
+ pip install echarts-china-cities-pypkg  

## Case 1: API介绍(OpenDataTools获取空气质量数据)

```python
from opendatatools import aqi

# 获取历史某日全国各大城市的AQI数据
# 返回DataFrame
df_aqi = aqi.get_daily_aqi('2018-05-27')
df_aqi.head(10)

# 获取实时全国各大城市的AQI数据
# 如果不指定时间点,会尝试获取最近的数据
#df_aqi = aqi.get_hour_aqi('2018-05-28 11:00:00')
df_aqi = aqi.get_hour_aqi()
df_aqi.head(10)

# 获取单个城市的AQI历史数据
df_aqi = aqi.get_daily_aqi_onecity('北京市')
df_aqi.head(10)

#获取单个城市某日的AQI小时数据
aqi_hour = aqi.get_hour_aqi_onecity('北京市', '2018-05-26')
aqi_hour.set_index('time', inplace=True)
aqi_hour.head(10)
```
我们可以得到如下的数据序列：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/get_daily_aqi.jpg)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/get_hour_aqi.jpg)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/get_daily_aqi_onecity.jpg)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/get_daily_aqi_onecity.jpg)

## Case 2 : 获取实时全国AQI数据并画地图展示

画图利用了开源的pyecharts组件。

```python
# encoding: utf-8

from opendatatools import aqi
from pyecharts import Geo

import pandas as pd

def draw_realtime_aqi_map(time = None):
    
    from opendatatools import aqi
    df_aqi = aqi.get_hour_aqi(time)

    # some city cannot by process by echart
    echart_unsupported_city = [
        "菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
        "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
        "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
        "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
        "昌吉州", "博州", "克州", "伊犁哈萨克州"]

    if time is None and len(df_aqi) > 0:
        time = df_aqi['time'][0]
    
    data = []
    for index, row in df_aqi.iterrows():
        city = row['city']
        aqi  = row['aqi']

        if city in echart_unsupported_city:
            continue

        data.append( (city, aqi) )

    geo = Geo("全国最新主要城市空气质量（AQI) - %s" % time , "数据来源于环保部网站",
              title_color="#fff",
              title_pos="center", width=1000,
              height=600, background_color='#404a59')

    attr, value = geo.cast(data)

    geo.add("", attr, value, visual_range=[0, 150], 
            maptype='china',visual_text_color="#fff",
            symbol_size=10, is_visualmap=True,
            label_formatter='{b}',             # 指定 label 只显示城市名
            tooltip_formatter='{c}',           # 格式：经度、纬度、值
            label_emphasis_textsize=15,        # 指定标签选中高亮时字体大小
            label_emphasis_pos='right'         # 指定标签选中高亮时字体位置
           )

    return geo

draw_realtime_aqi_map()
	
```
得到的图形如下：
![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/realtime_aqi_map.jpg)

### 点评：中国的空气污染，大多集中在北方地区。大首都治理空气质量，还是要下狠心啊。

## Case 3: 获取历史某日全国AQI数据并画地图展示

我们还可以画历史上任何一天的空气质量分布，代码如下：

```python
# encoding: utf-8

from opendatatools import aqi
from pyecharts import Geo

import pandas as pd


def draw_his_aqi_map(date):
    
    from opendatatools import aqi
    df_aqi = aqi.get_daily_aqi(date)
    #df_aqi.to_csv("aqi_daily.csv")

    # some city cannot by process by echart
    echart_unsupported_city = [
        "菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
        "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
        "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
        "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
        "昌吉州", "博州", "克州", "伊犁哈萨克州"]

    data = []
    for index, row in df_aqi.iterrows():
        city = row['city']
        aqi  = row['aqi']

        if city in echart_unsupported_city:
            continue

        data.append( (city, aqi) )

    geo = Geo("全国主要城市空气质量（AQI) - %s" % date , "数据来源于环保部网站",
              title_color="#fff",
              title_pos="center", width=1000,
              height=600, background_color='#404a59')

    attr, value = geo.cast(data)

    geo.add("", attr, value, visual_range=[0, 150], 
            maptype='china',visual_text_color="#fff",
            symbol_size=10, is_visualmap=True,
            label_formatter='{b}',             # 指定 label 只显示城市名
            tooltip_formatter='{c}',           # 格式：经度、纬度、值
            label_emphasis_textsize=15,        # 指定标签选中高亮时字体大小
            label_emphasis_pos='right'         # 指定标签选中高亮时字体位置
           )

    return geo

draw_his_aqi_map('2018-05-27')
	
```
得到的图形如下：
![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/his_aqi_map.jpg)

## Case 4 : 看某几个城市历史一段时间的走势图

再来看看不同城市的历史数据比较。

```python

# encoding: utf-8

from pyecharts import Line
import pandas as pd

def draw_city_aqi(cities, start_date = None, end_date = None):
    from opendatatools import aqi
    line = Line("城市AQI")
    
    data_dict = {}
    for city in cities:
        print("getting data for %s" % city)
        df_aqi = aqi.get_daily_aqi_onecity(city)
        df_aqi.set_index('date', inplace=True)
        df_aqi.sort_index(ascending=True, inplace=True)

        if start_date is not None:
            df_aqi = df_aqi[df_aqi.index >= start_date]
        
        if end_date is not None:
            df_aqi = df_aqi[df_aqi.index <= end_date]
        
        
        data_dict[city] = df_aqi
    
        axis_x = df_aqi.index
        axis_y = df_aqi['aqi']

        line.add("aqi curve for %s" % (city), axis_x, axis_y, mark_point=["average"])

    return line

draw_city_aqi(['北京市','上海市', '广州市', '深圳市', '三亚市'], start_date = '2018-01-01', end_date = '2018-05-31')
	
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/his_aqi_city.jpg)

三亚的确是人间天堂，深圳也很不错，大北京大上海大广州就要相形见绌了。

## Case 5 : 看某个城市日内小时走势图

在看看日内不同城市之间的比较.

```python
from pyecharts import Line
import pandas as pd

def draw_city_aqi_hour(cities, date):
    from opendatatools import aqi
    line = Line("城市AQI小时趋势图")
    
    data_dict = {}
    for city in cities:
        print("getting data for %s" % city)
        df_aqi = aqi.get_hour_aqi_onecity(city, date)
        df_aqi.set_index('time', inplace=True)
        df_aqi.sort_index(ascending=True, inplace=True)

        data_dict[city] = df_aqi
    
        axis_x = df_aqi.index
        axis_y = df_aqi['aqi']

        line.add("%s" % (city), axis_x, axis_y, mark_point=["average"])

    return line

draw_city_aqi_hour(['北京市', '上海市', '广州市', '深圳市', '三亚市'], '2018-05-28')
	
```

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/realtime_aqi_city.jpg)

#### 大北京，你今天发生了什么？如何让AQI从爆表变成优秀？

## 结尾彩蛋

1. opendatatools是quantos社区开发的轻量级的数据爬虫工具，后面会继续扩充功能，欢迎大家下载使用。

+ 项目地址: https://github.com/PKUJohnson/OpenData, 感兴趣的同学可以去研究代码.
+ 欢迎在www.quantos.org论坛反馈数据需求。

2. 欢迎关注我们的公众号：quantos

3. 完整的样例程序，请在www.quantos.org下载金融终端后获取。方法如下：

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/opendatatools/aqi/terminal_lecture.jpg)
