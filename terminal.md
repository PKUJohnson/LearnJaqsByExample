# quantos金融终端 - 可编程的金融终端

quantos开源社区的朋友们，今天我们重磅推出新产品“quantos金融终端 - 可编程的金融终端”。

## 为何要推出金融终端

简单来说，就是使用的体验更好，提高您的工作效率。

### 我们帮您整合了python运行环境

之前有很多朋友反馈，python环境安装、JAQS安装、python-snappy包安装经常会遇到问题，虽然我们推出了一键安装脚本，但还是有朋友会遇到奇怪的问题。

仔细思考之后，我们决定将python运行环境整合进金融终端（已经内置了必要的python包），免去用户安装的烦恼。

### 我们帮您整合了大量的优质内容

quantos社区提供了各种各样的产品，包括：
+ 开源软件DataCore、JAQS、tushare、vnpy
+ 内容产品“量化小学”、“量化24小时”
+ 各种优秀的研究成果
+ “微信公众号”、”微信群“、”官方网站“

quantos金融终端将这些内容有机整合在一起，方便用户获取和使用。

## 为何说是可编程的金融终端

用户每天都会接触到各类研究报告，里面有各种各样的结论，但大家都有一个疑问：

+ 1、这些报告的数据可靠吗？
+ 2、我怎么验证这些报告的结论？

虽有疑问，却很难去验证。

用户在学习金融课程的时候，希望能学习到一些在工作中实用的知识和技能。最有效的方法就是提供样例程序，code can talk。但这样高质量的课程依然太少。

quantos金融终端试图打破这种“尴尬”局面，打造“可编程金融终端”的理念。我们希望做到：

+ 1. 提供优秀研究成果的同时，提供样例代码。用户可下载到本地环境后进行验证。用户还可以在此基础上进行修改和完善，形成适合自己业务的研究成果。
+ 2. 提供优秀金融课程的同时，提供样例代码。用户可下载到本地环境后进行学习。
+ 3. 推广“可编程金融终端”的理念，让内容货真价实、让数据和代码说话。

## 如何使用金融终端

### 下载软件

请登录[官方网站](https://www.quantos.org)，进入“金融终端”频道，在“下载地址”里面，找到自己需要的版本。目前支持windows和mac两个平台。

网盘下载：
+ 试用版[quantos-mac.pkg](https://pan.baidu.com/s/1htKCTNY)
+ 试用版[quantos-win-x64.exe](https://pan.baidu.com/s/1bqL3efd)

官网下载:
+ 试用版[quantos-mac.pkg](http://downloads.quantos.org:9080/quantos-mac.pkg)
+ 试用版[quantos-win-x64.exe](http://downloads.quantos.org:9080/quantos-win-x64.exe)

### 安装软件

这个很简单，请按照安装向导，一步一步完成安装即可！Windows下建议把软件安装在D:盘，避免各种权限问题。

基础软件安装成功后，后续新版本可以自动更新。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/terminal_update.png)

### 登录

登录的用户名和密码就是您在quantos网站上注册的用户名和密码。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/terminal_login.png)

### 内容介绍

目前的版本是beta版，提供了“固收频道”、“教学频道”、“在线资源”、“本地环境”四个板块。未来优秀的内容会越来越多。

+ “固收频道”主要发布与固收研究有关的成果。
+ “教学频道”集成了“量化小学”、“量化24小时”两个专业课程。
+ “在线资源”是一些重要的网站的链接
+ “本地环境”是您的本地研究环境，下面重点介绍。

在每个内容频道中，都会提供“样例代码”，用户点击“样例代码”后，系统会把相应的代码下载到本地研究环境中，你就可以在本地环境中看到这个代码。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/terminal_samplecode.png)

每个样例代码都是一个“jupyter notebook”文件。

在“本地环境”中点击相应的“jupyter notebook”文件，终端会启动一个jupyter-notebook运行环境，用户可以修改和运行代码。

![](https://github.com/PKUJohnson/LearnJaqsByExample/blob/master/image/terminal_local.png)

你可以将样例的代码通过修改名称后，变成自己的代码。

### 一个小秘密

小伙伴们在使用quantos的DataApi和TradeApi时，都需要login，需要输入phone和token，在代码进行分享是，容易暴露自己的信息。

金融终端现在可以解决这个问题了。您只要在金融终端里面使用，可以这样获取phone和token

```python
import os
phone = os.environ.get('QUANTOS_USER')
token = os.environ.get('QUANTOS_TOKEN')
```

这样就再也不怕泄漏自己的电话号码了。


