---
layout: default
author: muyalei
date: 2018-12-25
title: sqoop的--options-file参数
tags:
   - sqoop相关
---


***整理自[https://segmentfault.com/a/1190000013928073](https://segmentfault.com/a/1190000013928073)***


### 将导入命令写入文件，通过 sqoop --options-file xx 完成导入

*参考实例*
```
import 
-D 
sqoop.hbase.add.row.key=true 
--connect 
jdbc:mysql://192.168.1.9:3306/spider 
--username 
root 
--password 
root 
--table 
TEST_GOODS 
--columns 
ID,GOODS_NAME,GOODS_PRICE 
--hbase-create-table 
--hbase-table 
tt_goods 
--column-family 
cf 
--hbase-row-key 
ID 
--where 
ID>=5 
-m 
1
```

*参数含义解释*
```
-D sqoop.hbase.add.row.key=true 是否将rowkey相关字段写入列族中，默认为false，默认情况下你将在列族中看不到任何row key中的字段。注意，该参数必须放在import之后。
--connect 数据库连接字符串
--username –password  mysql数据库的用户名密码
--table Test_Goods表名，注意大写
--hbase-create-table  如果hbase中该表不存在则创建
--hbase-table   对应的hbase表名
--hbase-row-key   hbase表中的rowkey,注意格式
--column-family   hbase表的列族
--where    导入是mysql表的where条件，写法和sql中一样
--split-by CREATE_TIME   默认情况下sqoop使用4个并发执行任务，需要制订split的列，如果不想使用并发，可以用参数 --m 1
```


### 定时增量导入

1. sqoop增量导入
```
sqoop import -D sqoop.hbase.add.row.key=true --connect jdbc:mysql://192.168.1.9:3306/spider --username root --password root --table TEST_GOODS --columns ID,GOODS_NAME,GOODS_PRICE --hbase-create-table --hbase-table t_goods --column-family cf --hbase-row-key ID --incremental lastmodified --check-column U_DATE --last-value '2017-06-27' --split-by U_DATE

--incremental lastmodified 增量导入支持两种模式 append 递增的列；lastmodified时间戳。
--check-column 增量导入时参考的列
--last-value 最小值，这个例子中表示导入2017-06-27到今天的值
```

2. sqoop job
```
sqoop job --create testjob01 --import --connect jdbc:mysql://192.168.1.9:3306/spider --username root --password root --table TEST_GOODS --columns ID,GOODS_NAME,GOODS_PRICE --hbase-create-table --hbase-table t_goods --column-family cf --hbase-row-key ID -m 1
```
设置定时执行以上sqoop job<br/>
使用linux定时器：crontab -e<br/>
例如每天执行<br/>
```
0 0 * * * /opt/local/sqoop-1.4.6/bin/sqoop job ….
--exec testjob01
```

### 数据从mysql导入hive中后，出现数据不一致情况

我们运行hadoop fs -cat /user/hadoop/student/part-m-00000,可以看到原来字段与字段之间都用‘,’分隔开，这是sqoop默认的，这时候，如果一个字段值当中包含‘,’，再向hive中插入数据时分隔就会出错。因为hive也是用‘,’分隔的。<br/>

解决方法：建议用‘001'来进行sqoop 导入数据时的 分割。也就是--fields-terminated-by <char>参数。

例子：
```
sqoop import --connect "jdbc:oracle:thin:@//localhost:1521/student" --password "***" --username "***" --query "select * from student where name='zhangsan' and class_id='003' and \$CONDITIONS" --target-dir "/user/hadoop/student" --fields-terminated-by "\001" --verbose -m 1
```





