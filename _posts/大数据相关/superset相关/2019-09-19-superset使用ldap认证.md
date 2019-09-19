---
layout: default
author: muyalei
title: superset使用ldap认证
date: 2019-09-19
tags:
    - superset
---


### 一、前言

superset的ldap认证设置这块儿，官方给出的指导文档有限，网上搜出来的配置方式也是五花八样，我本地实际测试后，都没能成功（没能成功的很大一部分原因是对我公司的ldap服务器配置没查证，默认ldap服务器配置是标准的来处理了）


### 二、安装superset

***1、anaconda安装。***</p >
略。
***2、使用pip工具安装。***</p >
整理自***[https://www.cnblogs.com/lovely-lisk/p/11411785.html](https://www.cnblogs.com/lovely-lisk/p/11411785.html)***</p >
防止链接页面丢失，主要过程整理如下：</p >
pip下载的依赖会按照其脚本找相应的版本，可能处于某些插件没有指定版本被下载了不兼容的版本的缘故，这里在此命令基础安装完成后对几个包的版本进行替换：</p >
1是pandas： pip install pandas==0.23.4</p >
2是flask-jwt-extended：pip install flask-jwt-extended==3.10.0</p >
3是flask-appbuilder：pip install flask-appbuilder==1.12.1 #基础思想就是改版本直到红字消失,可能每个人的环境会有不同，记住这是方法和思路</p >
4是SQLAlchemy：pip install sqlalchemy==1.2.18</p >

初始化superset：</p >
```
#一些基本设定
python fabmanager create-admin --app superset  

#初始化数据库
python superset db upgrade  

#载入样例
python superset load_examples  

#初始化role and power
python superset init 

#启动服务-p是设置端口，默认8088
python superset runserver -p 3000 -d
```

 
