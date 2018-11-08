---
layout: default
autor: muyalei
date: 2018-10-30
title: mariaDB安装完成后设置root密码等初始化操作
tags:
   - mysql
---

***转载自[https://www.cnblogs.com/LvLoveYuForever/p/5585197.html](https://www.cnblogs.com/LvLoveYuForever/p/5585197.html)***

#### 修改root密码
1.以root身份在终端登陆(必须)

2.输入 mysqladmin -u root -p password ex
后面的 ex 是要设置的密码

3.回车后出现 Enter password 
输入就密码，如果没有，直接回车

 

打开远程访问权限

MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '123456' WITH GRANT OPTION;
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> flush privileges;
Query OK, 0 rows affected (0.00 sec)

如果远程还是没有办法访问，那就开启3306端口就行：

[root@marslv yum.repos.d]# iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
[root@marslv yum.repos.d]# service iptables save
[root@marslv yum.repos.d]# service iptables restart

 

创建用户
//创建用户
mysql> insert into mysql.user(Host,User,Password) values("localhost","admin",password("admin"));
//刷新系统权限表
mysql>flush privileges;
这样就创建了一个名为：admin  密码为：admin  的用户。

创建数据库(在root权限下)
create database mydb;
//授权admin用户拥有mydb数据库的所有权限。
>grant all privileges on mydb.* to admin@localhost identified by 'admin';
//刷新系统权限表
mysql>flush privileges;

删除用户。
@>mysql -u root -p
@>密码
mysql>DELETE FROM user WHERE User="admin" and Host="localhost";
mysql>flush privileges;
//删除用户的数据库
mysql>drop database mydb;

修改指定用户密码。
@>mysql -u root -p
@>密码
mysql>update mysql.user set password=password('新密码') where User="admin" and Host="localhost";

mysql>flush privileges;
