---
layout: default 
authoer: muyalei 
date: 2018-12-21
title: 带有blob字段类型的mysql表导入hive
tags:
   - sqoop相关
---

两种办法
1. 从mysql导出时，把BLOB转成STRING保存
2. 在HADOOP端实现mysql BLOB的解析方法，HIVE访问时，用UDF函数动态处理这些数据。
第一个办法更简单。


mysql的blob字段类型不能通过sqoop直接导入hive。可以先用sqoop将mysql数据导入到hdfs，之后在hive建立空表，再通过load data做映射。

详细可以参考 [https://blog.csdn.net/kwu_ganymede/article/details/49096695](https://blog.csdn.net/kwu_ganymede/article/details/49096695)
