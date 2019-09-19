---
layout: default
author: muyalei
date: 2018-12-21
title: 使用sqoop --options-file xx 导入hive数据
tags:
   - sqoop相关
---


***整理自[https://blog.csdn.net/kwu_ganymede/article/details/49095453](https://blog.csdn.net/kwu_ganymede/article/details/49095453)***


### 使用sqoop --options-file直接导入hive数据，把操作命令语句写在文件中，便于管理及管理

1. 创建hive数据库及表
```
create database DB_TEST;

CREATE TABLE UserRegLoginLog
    (
        ID BIGINT,
        fld_date TIMESTAMP,
        fld_ip string,
        fld_server_ip string,
        fld_UA string,
        UserId BIGINT ,
        UserName string,
        PassWord string,
        ActionType INT ,
        ActionTime TIMESTAMP ,
        ActionIP string,
        FromHost string,
        UrlRefer string,
        RemotePort string
    )
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' ;
```

2. 编写sqoop操作文件，注意做分隔符需要与hive的一致
```
vi UserRegLoginLog_hive.opt  

import 
--connect 
jdbc:jtds:sqlserver://localhost:1433;;DatabaseName=DB_TEST 
--username 
sa 
--password 
123456
--table 
UserRegLoginLog
--where
1=1
--columns
" ID ,fld_date ,fld_ip ,fld_server_ip ,fld_UA ,UserId  ,UserName ,PassWord ,ActionType  ,ActionTime  ,ActionIP ,FromHost ,UrlRefer,RemotePort "
--fields-terminated-by 
'\t'
--hive-import
--hive-overwrite
--hive-drop-import-delims
--hive-table
DB_TELECAST.UserRegLoginLog
```

使用sqoop --options-file 执行操作文本
```
sqoop --options-file ./UserRegLoginLog_hive.opt
```


3. 指定hive的数据库，格式为: 数据库.表名

DB_TEST.UserRegLoginLog


