---
layout: default
author: muyalei
date: 21018-12-03
title: 操作redis之HyperLogLog
tags:
   - redis
---

***整理自[http://www.cnblogs.com/xuchunlin/p/7097272.html](http://www.cnblogs.com/xuchunlin/p/7097272.html)***

```
#coding:utf8
import redis
# python 操作redis之——HyperLogLog
r =redis.Redis(host="33.23.724.12190",port=6222,password="666666")
```
1.Pfadd 命令将所有元素参数添加到 HyperLogLog 数据结构中。
```
print r.pfadd("1","1","2")  #输出结果是1
print r.pfadd("1","3","4")  #输出结果是1
print r.pfadd("1","4","5")  #输出结果是1
```

2. Pfcount 命令返回给定 HyperLogLog 的基数估算值。
```
print r.pfcount("1")        #输出结果是5, 因为 4 重复了两次
print r.pfcount("2")        #输出结果是0,
```


