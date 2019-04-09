---
layout: default
author: muyalei
time: 2019-04-09
title: python获取当前主机ip、mac地址
tags:
   - python相关
---


***整理自[https://blog.csdn.net/chengqiuming/article/details/78601150](https://blog.csdn.net/chengqiuming/article/details/78601150)***


mac地址提取：
```
macHex = uuid.UUID(int=uuid.getnode()).hex[-12:]
mac = "-".join([macHex[e:e+2] for e in range(0,11,2)])
```


ip提取：
```
ip = socket.gethostbyname(socket.gethostname())
```



























