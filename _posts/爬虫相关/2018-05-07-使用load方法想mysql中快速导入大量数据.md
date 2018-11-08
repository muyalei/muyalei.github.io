---
layout:     post
title:      使用load方法向mysql中快速导入大量数据
subtitle:   mysql使用
date:       2018-05-07
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - mysql
---

### 将数据从mysql迁移到另一个mysql
1.进入mysql，直接执行 source xx.sql ，将从另一个库中下载下来的数据导入目标库。
  缺点：速度很慢。

2.进入mysql，使用如下例所示命令：
  ```
  LOAD DATA local INFILE '/tmp/myl/tbl_china_street.txt' IGNORE INTO TABLE tbl_china_street FIELDS TERMINATED BY '\t' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' ignore 1 lines(streetUrl_key,city,adminRegion,streetName,position,status,createStamp,actionStamp);
  ```
  优点：速度极快！
  
  注意： LINES TERMINATED BY '\r\n' 这里，如果是windows系统上的 .txt 文件导入linux平台的mysql库中，分隔符要使用 '\r\n'，如果是 类Unix 向linux导入，
  分隔符使用 '\n'。（分割符使用错误，可能会出现只插入1条数据，或只能插入1半数据的情况（如有3万条数据，却只能插入1.5万条！））
  
  具体使用请参考：[https://blog.csdn.net/caoxiaohong1005/article/details/72571798](https://blog.csdn.net/caoxiaohong1005/article/details/72571798)
  
### 错误处理
使用第2种方式导入数据时，可能会出现如下错误：
```
1197, HY000, Multi-statement transaction required more than 'max_binlog_cache_size' bytes of storage; increase this mysqld variable and try again
```
####### 解决办法
修改my.cnf，增大binlog_cache_size和max_binlog_cache_size参数的值
```
binlog_cache_size = 20M
max_binlog_cache_size = 100M
```
具体内容参考[https://www.cnblogs.com/MYSQLZOUQI/p/6820688.html](https://www.cnblogs.com/MYSQLZOUQI/p/6820688.html)




