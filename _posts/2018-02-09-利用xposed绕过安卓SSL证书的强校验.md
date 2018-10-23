---
layout:     post
title:      利用xposed绕过安卓SSL证书的强校验
subtitle:   
date:       2018-02-09
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - 手机App数据采集
    - 抓包
---

### 什么是SSL pinning

https协议验证服务器身份的方式通常有三种，一是根据浏览器或者说操作系统（Android）自带的证书链；二是使用自签名证书；三是自签名证书加上SSL Pinning特性。第一种需要到知名证书机构购买证书，需要一定预算。第二种多见于内网使用。第三种在是安全性最高的，但是需要浏览器插件或客户端使用了SSL Pinning特性。

Android应用程序在使用https协议时也使用类似的3种方式验证服务器身份，分别是系统证书库、自带证书库、自带证书库 + SSL Pinning特性。

所以SSL Pinning，即SSL证书绑定，是验证服务器身份的一种方式，是在https协议建立通信时增加的代码逻辑，它通过自己的方式验证服务器身份，然后决定通信是否继续下去。它唯一指定了服务器的身份，所以安全性较高。

我们可以使用xposed框架来绕过SSL Pinning，使用JustTrustMe模块。


## JustTrustMe
当客户端使用了SSL pinning的时候，手机导入burpsuite证书的方式也无法抓到通信包。除了修改apk验证证书逻辑重新打包的方式外，最简单的方法是使用xposed相关模块。

xposed安装方法：

[下载xposed安装包](http://repo.xposed.info/module/de.robv.android.xposed.installer)

安装xposed框架到手机：

```adb install <xposed-installer-you-just-downloaded>.apk```    

安装并启用[justtrustme模块](https://github.com/Fuzion24/JustTrustMe)

注意，安装justtrustme后，需要勾选上，才算启用:
![2018-02-09-利用xposed绕过安卓SSL证书的强校验_图片.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-09-%E5%88%A9%E7%94%A8xposed%E7%BB%95%E8%BF%87%E5%AE%89%E5%8D%93SSL%E8%AF%81%E4%B9%A6%E7%9A%84%E5%BC%BA%E6%A0%A1%E9%AA%8C_%E5%9B%BE%E7%89%87.jpg)
重启手机就可以抓到之前抓不到的https通信了。

参考资料：
- [绿盟Security2015/07总029期](http://www.nsfocus.com.cn/upload/contents/2015/07/2015_07241353337959.pdf)
- [对抗Android SSL Pinning](http://www.nsfocus.com.cn/upload/contents/2015/07/2015_07241441569651.pdf)

转自[xdxd](http://xdxd.love/2015/12/30/%E5%88%A9%E7%94%A8xposed%E7%BB%95%E8%BF%87%E5%AE%89%E5%8D%93SSL%E8%AF%81%E4%B9%A6%E7%9A%84%E5%BC%BA%E6%A0%A1%E9%AA%8C/)、[独自等待](https://www.waitalone.cn/bypass-ssl-pinning.html)，略有改动。
