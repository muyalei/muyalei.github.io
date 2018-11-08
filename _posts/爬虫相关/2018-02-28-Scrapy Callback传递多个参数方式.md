---
layout:     post
title:      Scrapy Callback传递多个参数方式
subtitle:   
date:       2018-02-28
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - scrapy
---

转自[http://blog.csdn.net/Haihao_micro/article/details/78529370](http://blog.csdn.net/Haihao_micro/article/details/78529370)

在scrapy提交一个链接请求是用 Request(url,callback=func) 这种形式的，而func只有一个response参数，如果自定义一个有多参数的func可以考虑用下面的方法实现多个参数传递。

```
def parse(self,response):
    yield Request(url, callback=lambda response, typeid=5: self.parse_type(response,typeid))

def parse_type(self,response, typeid):
    print typeid
```

将参数写在lambda里面封装一下就行，内函数有多少个需要传递的参数在lambda里面就需要写多少个，加上默认值就好，如果直接写到内函数会变成形参。


