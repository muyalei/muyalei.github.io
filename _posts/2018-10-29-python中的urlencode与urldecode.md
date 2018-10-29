---
layout: default
author: muyalei
date: 2018-10-29
title: python中的urlencode与urldecode
tags:
   - python模块
---

转载自[http://www.cnblogs.com/caicaihong/p/5687522.html](http://www.cnblogs.com/caicaihong/p/5687522.html)

当url地址含有中文，或者参数有中文的时候，这个算是很正常了，但是把这样的url作为参数传递的时候（最常见的callback），需要把一些中文甚至'/'做一下编码转换。

所以对于一些中文或者字符，url不识别的，则需要进行转换，转换结果如下：

一、urlencode
urllib库里面有个urlencode函数，可以把key-value这样的键值对转换成我们想要的格式，返回的是a=1&b=2这样的字符串，比如：
```
import urllib.parse
values={}
values['username']='02蔡彩虹'
values['password']='ddddd?'
url="http://www.baidu.com"
data=urllib.parse.urlencode(values)
print(data)
#结果如下
username=02%E8%94%A1%E5%BD%A9%E8%99%B9&password=ddddd%3F
```

如果只想对一个字符串进行urlencode转换，怎么办？urllib提供另外一个函数：quote()
```
import urllib.parse
s='长春'
s=urllib.parse.quote(s)
print(s)
#输出结果为：
%E9%95%BF%E6%98%A5
```
二、urldecode
当urlencode之后的字符串传递过来之后，接受完毕就要解码了——urldecode。urllib提供了unquote()这个函数，可没有urldecode()！
```
s='%E5%B9%BF%E5%B7%9E'
s=urllib.parse.unquote(s)
print(s)
#输出结果为：
广州
```

