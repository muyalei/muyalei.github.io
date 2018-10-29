---
layout: default
author: muyalei
date: 2018-10-29
title: mac系统下安装secureCRT
tag: 
   - 工具安装
---

文章转载自[https://www.cnblogs.com/python-nameless/p/6925579.html](https://www.cnblogs.com/python-nameless/p/6925579.html)

1. 先[下载SecureCRT和破解文件]()默认下载到了当前用户的”下载”目录中

2. 在”Finder”中 打开 “scrt-7.3.0-657.osx_x64.dmg” 并将 SecureCRT复制到”应用程序”中. 这时SecureCRT的路径是: /Applications/SecureCRT.app/Contents/MacOS/SecureCRT

3. 测试一下SecureCRT是否能打开, 如果可以,先关闭

4.在终端中输入 sudo perl ~/Downloads/securecrt_mac_crack.pl /Applications/SecureCRT.app/Contents/MacOS/SecureCRT  
>注意： 具体目录地址根据自己而定。

5. 如果终端中有输出下面的信息, 表示激活成功了
```
It has been cracked 
License: 
Name: bleedfly 
Company: bleedfly.com 
Serial Number: 03-29-002542 
License Key: ADGB7V 9SHE34 Y2BST3 K78ZKF ADUPW4 K819ZW 4HVJCE P1NYRC 
Issue Date: 09-17-2013
```
6. 打开SecureCRT，输入刚才终端的数据就完成了破解

　　再次打开 SecureCRT 点击Enter License Data..

　　1) 直接Continue，空白不填写

　　2) 点击Enter Licence Manually

　　3) Name:输入bleedfly Company:输入 bleedfly.com

　　4) Serial number: 03-29-002542
 
　　　 License key: ADGB7V 9SHE34 Y2BST3 K78ZKF ADUPW4 K819ZW 4HVJCE P1NYRC

　　5) Issue date: 09-17-2013

　　6) 点击 Done

7. 激活完成。
