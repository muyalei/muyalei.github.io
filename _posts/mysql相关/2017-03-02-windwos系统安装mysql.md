----
layout: default
author: muyalei
date: 2018-03-02
title: windows系统安装mysql
tags:
   - mysql
---

***转载自[https://jingyan.baidu.com/article/8ebacdf02e392a49f65cd52d.html](https://jingyan.baidu.com/article/8ebacdf02e392a49f65cd52d.html)***

先下载安装包，然后进行下面的操作，官网有最新安装包。下面是安装教程以及更换mysql5.6.27.0安装路径的方法。（关于applying security settings错误解决、以及彻底删除mysql重新安装的方式在安装教程下面。）

![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片1.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片1.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片2.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片2.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片3.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片3.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片4.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片4.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片5.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片5.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片6.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片6.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片7.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片7.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片8.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片8.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片9.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片9.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片10.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片10.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片11.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片11.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片12.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片12.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片13.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片13.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片14.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片14.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片15.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片15.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片16.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片16.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片17.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片17.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片18.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片18.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片19.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片19.jpg)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片20.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-02-windows系统安装mysql_图片/2017-03-02-windows系统安装mysql_图片20.jpg)

下面这里是解决关于applying security settings错误解决(网上一般的解决方案是说这样是因为不彻底删除mysql造成的。所以，这个错误的解决方案与删除mysql的内容一样)、以及彻底删除mysql重新安装的方式


