---
layout: default
author: muyalei
title: 雷电模拟器安装xposed框架
date: 2021-09-29
tags:
	- 爬虫相关
---

**整理自：**[https://blog.csdn.net/weixin_44183483/article/details/118931351](https://blog.csdn.net/weixin_44183483/article/details/118931351)


直接官方下载安装启动，然后在雷电游戏中心下载xposed框架，然后打开，会发现没有激活，

[](雷电模拟器安装xposed框架_1)

打开[https://dl-xda.xposed.info/framework/](https://dl-xda.xposed.info/framework/)：

[](雷电模拟器安装xposed框架_2)

选择sdk版本： 查看自己系统版本是多少，我的系统版本是7.1.2 直接网上搜索android个版本对应的sdk版本，所以我的sdk版本是sdk25：

[](雷电模拟器安装xposed框架_3)

我们由于是模拟器所以选择x86，如果是自己的真机的话，就算选择arm64 现在大部分手机都是64位的。接下来选择倒数第二个进行下载：

[](雷电模拟器安装xposed框架_4)

[](雷电模拟器安装xposed框架_5)

下载成功后进行解压。

新建一个文件夹xposed ，将上面的解压后的文件中system文件拷贝到xposed中。通过 https://forum.xda-developers.com/attachment.php?attachmentid=4489568&d=1525092710 链接下载scrapy.txt文件，并改名为scrapy.sh，将scrapy.sh 放在新建xposed文件夹中。

以此输入adb命令：
```
adb remount
adb push xposed /system
adb shell
su
cd /system/xposed
mount -o remount -w /system
sh script.sh
```
然后重启一下虚拟机，打开xposed，已经激活：

[](雷电模拟器安装xposed框架_6)