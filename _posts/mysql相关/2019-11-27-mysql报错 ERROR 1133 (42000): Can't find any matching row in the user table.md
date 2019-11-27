---
layout: default
author: muyalei
title: --
date: 2019-11-27
tags:
    - mysql
---


***整理自[https://blog.csdn.net/ljw_jiawei/article/details/90784350](https://blog.csdn.net/ljw_jiawei/article/details/90784350)***


1、问题描述
使用set password for 'root'@'localhost'=password('MyNewPass4!'); 命令修改mysql数据库root用户密码提示**ERROR 1133 (42000): Can't find any matching row in the user table**错误

2、主要原因
错误提示的字面意思：在用户表中找不到任何匹配的行

登录mysql执行以下命令

use mysql;
select Host,User from user;


主要原因是修改密码的条件不否

3、解决办法
将set password for 'root'@'localhost'=password('MyNewPass4!'); 代码中的localhost修改%，与数据库Host字段值一致
set password for 'root'@'%'=password('MyNewPass4!');
刷新
flush privileges;

密码已修改成功









