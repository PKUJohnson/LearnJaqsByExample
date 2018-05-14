# 人工智能在身边

周末，由于工作需要研究了一下自动翻译，还是非常的实用和有效，分享给大家。

## 语言翻译的刚性需求

+ 在日常的工作中，常常会遇到跨语言翻译的需求。
+ 专业商务词汇的翻译就更加困难一些。
+ 语言间的自动翻译属于自然语言处理（NLP）的一个分支，算是人工智能的一个具体应用。
+ 自动翻译算法涉及语法分析、感情分析、语境分析、上下文分析等专业技术，是一个很有学术含量的课题。

目前语言自动翻译的研究成果已经很多，Google、Baidu、网易等公司都推出了自己的在线翻译服务。

## 如何在程序中应用自动翻译

这里介绍一下我使用的百度翻译开放平台，其他公司的产品类似，平台特点如下：

+ 百度翻译开放平台[官方网站](https://fanyi-api.baidu.com/api/trans/product/index)
+ 支持28种语言实时互译，覆盖中、英、日、韩、西、法、泰、阿、俄、葡、德、意、荷、芬、丹等
+ 提供通用翻译API
+ 每月免费翻译字符数额度200万，超过额度需要收费

## 代码样例(英译中)

+ 要用API，首先要申请自己的appid和secret。
+ 详细的API文档，请参考[这里](https://fanyi-api.baidu.com/api/trans/product/apidoc#joinFile)

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/baidu_translation_api.png)

代码样例（英译中）：

```python
import requests
import json
import hashlib
import time

def translation(q):
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    appid  = "get your appid  from web"
    secret = "get your secret from web"
    salt   = "12345678"

    hl = hashlib.md5()
    text = appid+q+salt+secret
    hl.update(text.encode("utf-8"))
    sign = hl.hexdigest()

    param = {
        "q"      : q,
        "from"   : "en",
        "to"     : "zh",
        "appid"  : appid,
        "salt"   : salt,
        "sign"   : sign,
    }
    session = requests.session()
    session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    response = session.get(url, params = param)
    rsp = json.loads(response.text)
    return rsp["trans_result"][0]['dst']
```

## 应用效果

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/translation.gif)

翻译还是非常准确的，大家可以自己去试试。（用多了需要付费哦！！！）

## 有感

+ 科技发展非常迅速，大学期间自动翻译还是一个前沿的研究课题，现在已经完全是成熟的产品了。
+ 科技应用好了，会大大造福人类。像自动翻译、语音识别、机器人等人工智能技术和产品，正一点一滴的融入人类生活。
+ 科技只是工具，如果价值观发生了偏差，也会造成很多社会问题。像滴滴的顺风车、腾讯的王者毒药、快手头条的低俗视频、百度的医疗广告，都是值得警惕的。

