---
layout: default
author: muyalei
date: 2019-01-24
title: mysql的binlog详解
tags:
   - mysql相关
---


***整理自[https://www.cnblogs.com/xhyan/p/6530861.html](https://www.cnblogs.com/xhyan/p/6530861.html)***

Mysql的binlog日志作用是用来记录mysql内部增删改查等对mysql数据库有更新的内容的记录（对数据库的改动），对数据库的查询select或show等不会被binlog日志记录;主要用于数据库的主从复制以及增量恢复。

mysql的binlog日志必须打开log-bin功能才能生存binlog日志<br/>
-rw-rw---- 1 mysql mysql   669 8月  10 21:29 mysql-bin.000001<br/>
-rw-rw---- 1 mysql mysql   126 8月  10 22:06 mysql-bin.000002<br/>
-rw-rw---- 1 mysql mysql 11799 8月  15 18:17 mysql-bin.000003<br/>

### 1、打开MySQL的log-bin功能

编辑my.cnf配置文件
```
# grep log-bin my.cnf
log-bin = /data/3306/mysql-bin
```
查看是否启用了日志
```
mysql>show variables like 'log_bin';
```
### 2、Mysqlbinlog解析工具

　　Mysqlbinlog功能是将Mysql的binlog日志转换成Mysql语句，默认情况下binlog日志是二进制文件，无法直接查看。<br/>
　　Mysqlbinlog参数<br/>
参数	                            描述<br/>
-d	                                指定库的binlog<br/>
-r	                                相当于重定向到指定文件<br/>
--start-position--stop-position	    按照指定位置精确解析binlog日志（精确），如不接--stop-positiion则一直到binlog日志结尾<br/>
--start-datetime--stop-datetime	    按照指定时间解析binlog日志（模糊，不准确），如不接--stop-datetime则一直到binlog日志结尾<br/>
备注：myslqlbinlog分库导出binlog，如使用-d参数，更新数据时必须使用use database。<br/>

例：解析ceshi数据库的binlog日志并写入my.sql文件
```
#mysqlbinlog -d ceshi mysql-bin.000003 -r my.sql
```
使用位置精确解析binlog日志
```
#mysqlbinlog mysql-bin.000003 --start-position=100  --stop-position=200 -r my.sql
```

### 3、MySQL binlog的三种工作模式

　　（1）Row level<br/>
　　日志中会记录每一行数据被修改的情况，然后在slave端对相同的数据进行修改。<br/>
　　优点：能清楚的记录每一行数据修改的细节<br/>
　　缺点：数据量太大<br/>
　　（2）Statement level（默认）<br/>
　　每一条被修改数据的sql都会记录到master的bin-log中，slave在复制的时候sql进程会解析成和原来master端执行过的相同的sql再次执行<br/>
　　优点：解决了 Row level下的缺点，不需要记录每一行的数据变化，减少bin-log日志量，节约磁盘IO，提高新能<br/>
　　缺点：容易出现主从复制不一致<br/>
　　（3）Mixed（混合模式）<br/>
　　结合了Row level和Statement level的优点<br/>

### 4、MySQL企业binlog模式的选择

1.互联网公司使用MySQL的功能较少（不用存储过程、触发器、函数），选择默认的Statement level<br/>
2.用到MySQL的特殊功能（存储过程、触发器、函数）则选择Mixed模式<br/>
3.用到MySQL的特殊功能（存储过程、触发器、函数），又希望数据最大化一直则选择Row模式<br/>

### 5、设置MySQL binlog模式

- 查看MySQLbinlog模式
```
mysql>show global variables like "binlog%";
+-----------------------------------------+-----------+
| Variable_name                           | Value     |
+-----------------------------------------+-----------+
| binlog_cache_size                       | 1048576   |
| binlog_direct_non_transactional_updates | OFF       |
| binlog_format                           | STATEMENT |       #系统默认为STATEMENT模式
| binlog_stmt_cache_size                  | 32768     |
+-----------------------------------------+-----------+
4 rows in set (0.00 sec)　
```

- MySQL中设置binlog模式
```
mysql>set global binlog_format='ROW';　　
```
配置文件中设置binlog模式
```
#vim my.cnf
[mysqld]
binlog_format='ROW'          #放在mysqld模块下面
user    = mysql
port    = 3306
socket  = /data/3306/mysql.sock
```

### 6、配置完成后需要重启mysql服务

Row模式下解析binlog日志
```
#mysqlbinlog --base64-output="decode-rows" -v mysql-bin.000001
```
