---
layout: default
author: muyalei
title: ssh登录或者启动hadoop、hbase时报错"ECDSA host key for ip has changed"的解决方法
date: 2019-10-24
tags:
  - 大数据相关
---

***整理自[https://blog.csdn.net/yunweifun/article/details/78763026](https://blog.csdn.net/yunweifun/article/details/78763026)***

当我们使用ssh root@ip登录Linux服务器时，服务器报错：

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:Ms+BRn93GbOO1fwP6g1O+UwSRFv9KIUMGeoHDt70OfQ.
Please contact your system administrator.
Add correct host key in /Users/aliyunbaike/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/aliyunbaike/.ssh/known_hosts:6
ECDSA host key for 47.74.190.156 has changed and you have requested strict checking.
Host key verification failed.
```

这是由于，ssh连接服务器时，如果之前连接过，ssh会默认保存该ip的连接协议信息，当我们再次访问此ip服务器时，ssh会自动匹配之前ssh保存的信息，由于我们的服务器做了更改，例如重装系统等操作，会导致本地保存的ssh信息失效，于是再次连接时就会出现上述错误。

另外，远程服务器的ssh服务被卸载重装或ssh相关数据（协议信息）被删除也会导致这个错误。



解决方案：

删除本地known_hosts里面的缓存信息即可。命令：ssh-keygen -R "你的远程服务器ip地址"  

注意：R是大写！
