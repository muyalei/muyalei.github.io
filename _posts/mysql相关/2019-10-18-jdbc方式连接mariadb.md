---
layout: default
author: muyalei
title: jdbc方式连接mariadb
date: 2019-10-18
tags:
  - mysql相关
---


***整理自[https://blog.csdn.net/wwwdc1012/article/details/52749188](https://blog.csdn.net/wwwdc1012/article/details/52749188)***


java连接mariaDB数据库的设置：(tomcat 8)

### 第一种方法：使用tomcat自带的mysql-connector-java-5.1.40-bin.jar

下载地址：[https://dev.mysql.com/downloads/connector/j/5.1.html](https://dev.mysql.com/downloads/connector/j/5.1.html)

java代码中的设置：</p>
driver驱动类为：com.mysql.jdbc.Driver</p>
url为： jdbc:mysql://localhost:3306/dbName</p>
```
String driver =“com.mysql.jdbc.Driver”;
//从配置参数中获取数据库url
String url = “jdbc:mysql://localhost:3306/dbName”;
//从配置参数中获取用户名
String user = “root";
//从配置参数中获取密码
String pass = "pass";

//注册驱动
Class.forName(driver);
//获取数据库连接
Connection conn = DriverManager.getConnection(url,user,pass);
//创建Statement对象
Statement stmt = conn.createStatement();
//执行查询
ResultSet rs = stmt.executeQuery("select * from news_inf");
```

### 第二种，使用mariadb的jdbc Driver

需要下载jdbc连接器mariadb-java-client-1.5.2.jar</p>
网址：[https://mariadb.com/download_file/connector/java/mariadb-java-client-1.5.2.jar](https://mariadb.com/download_file/connector/java/mariadb-java-client-1.5.2.jar)

将文件复制到应用的WEB-INF下(只在本应用使用)或复制到tomcat的lib文件夹下（所有应用可使用）

上面那段代码 ，driver驱动类为：org.mariadb.jdbc.Driver</p>
url为：jdbc:maria://localhost:3306/dbName


