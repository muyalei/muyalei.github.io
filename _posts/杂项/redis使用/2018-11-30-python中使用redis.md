---
layout: default
author: muyalei
date: 2018-11-30
title: python中使用redis
tags:
   - python相关
---

使用实例：

```
import redis

db = redis.Redis(host='x.x.x.x',port='6379')

db.llen('testList')
```
