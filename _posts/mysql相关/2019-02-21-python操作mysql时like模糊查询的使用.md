---
layout: default
author: muyalei
date: 2019-02-21
title: python操作mysql时like模糊查询的使用
tags:
  - 爬虫相关
---


示例：
```
cityName = '北京'
sqli = 'select count(1) from `tbl_basic_shop_info` where city like "%%' + cityName + '%%"'
self.cursor.execute(sqli)
```
