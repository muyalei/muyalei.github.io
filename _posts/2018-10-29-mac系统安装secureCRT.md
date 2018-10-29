---
layout: default
author: muyalei
date: 2018-10-29
title: mac系统下安装secureCRT
tag: 
   - 工具安装
---

1. 先[下载SecureCRT和破解文件]()默认下载到了当前用户的”下载”目录中
2. 在”Finder”中 打开 “scrt-7.3.0-657.osx_x64.dmg” 并将 SecureCRT复制到”应用程序”中. 这时SecureCRT的路径是: /Applications/SecureCRT.app/Contents/MacOS/SecureCRT
3. 测试一下SecureCRT是否能打开, 如果可以,先关闭
4.在终端中输入 sudo perl ~/Downloads/securecrt_mac_crack.pl /Applications/SecureCRT.app/Contents/MacOS/SecureCRT  
>注意： 具体目录地址根据自己而定。
5. 如果终端中有输出下面的信息, 表示激活成功了
