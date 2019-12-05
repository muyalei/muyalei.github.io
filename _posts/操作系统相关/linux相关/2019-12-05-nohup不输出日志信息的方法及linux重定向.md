---
layout: default
author: muyalei
title: nohup不输出日志信息的方法及linux重定向
date: 2019-12-05
tags:
    - linux
---

***整理自[https://www.cnblogs.com/zhangchao0515/p/9771506.html](https://www.cnblogs.com/zhangchao0515/p/9771506.html)***

最近使用nohup创建了一个后台进程，默认日志输出到了nohup.out文件中，程序跑起来也就没再管，过了大约一周，发现硬盘空间不够了，于是查找原因，发现这个nohup.out文件已经到了70G了，导致硬 盘空间不足了。
解决方案

只输出错误信息到日志文件
```
nohup ./program >/dev/null 2>log &
```
什么信息也不要
```
nohup ./program >/dev/null 2>&1 &
```
知识补充，关于Linux的重定向

Linux的3中重定向
```
0:表示标准输入
1:标准输出,在一般使用时，默认的是标准输出
2:标准错误信息输出
```

可以用来指定需要重定向的标准输入或输出。例如，将某个程序的错误信息输出到log文件 中：./program 2>log。这样标准输出还是在屏幕上，但是错误信息会输出到log文件中。另外，也可 以实现0，1，2之间的重定向。2>&1：将错误信息重定向到标准输出。
关于/dev/null文件

Linux下还有一个特殊的文件/dev/null，它就像一个无底洞，所有重定向到它的信息都会消失得无影 无踪。这一点非常有用，当我们不需要回显程序的所有信息时，就可以将输出重定向到/dev/null。





