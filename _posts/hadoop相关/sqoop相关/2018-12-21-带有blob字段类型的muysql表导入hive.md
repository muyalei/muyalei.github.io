---
layout: default 
authoer: muyalei 
date: 2018-12-21
title: 带有blob字段类型的mysql表导入hive
tags:
   - sqoop相关
---

mysql的blob字段类型不能通过sqoop直接导入hive。可以先用sqoop将mysql数据导入到hdfs，之后在hive建立空表，再通过load data做映射。

详细可以参考 [https://blog.csdn.net/kwu_ganymede/article/details/49096695](https://blog.csdn.net/kwu_ganymede/article/details/49096695)
