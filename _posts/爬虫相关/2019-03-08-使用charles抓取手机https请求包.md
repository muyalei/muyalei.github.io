---
layout: default
author: muyalei
date: 2019-03-08
title: 使用charles抓取手机https请求包
tags:
   - 抓包
---


***转自[https://www.cnblogs.com/meitian/p/7157990.html](https://www.cnblogs.com/meitian/p/7157990.html)***


### 安装破解版Charles
 
下载破解版包，先启动一次未破解版的Charles，然后再替换包内容的java下的Charles.jar
 
![2019-03-08-使用charles抓取手机https请求包_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%871.png)

破解版下载地址（如果不幸的又不能下载了，那就网上随便搜一个吧）：

http://download.csdn.net/download/m694449212/9770583

https://pan.baidu.com/share/link?shareid=2768818025&uk=1281550132

第二个网址为破解的charless.jar，第一个下载地址中的有点问题


### 手机通过Charles抓取https
  
第一步：配置Charles，允许抓取https包
Proxy->SSL Proxying Settings…，勾选Enable SSL Proxying，Add一个locations，通过通配符\* 抓取所有域名的https。（如果想只抓取某个域名的，设置具体域名的即可）

![2019-03-08-使用charles抓取手机https请求包_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%872.png)
![2019-03-08-使用charles抓取手机https请求包_图片3.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%873.png)
![2019-03-08-使用charles抓取手机https请求包_图片4.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%874.png)

Host可以使用通配符\*或?进行匹配，如果想抓取所有域名的，直接用\*即可(Add一个新的Location，然后直接点OK就创建了)，如果特定想抓取某个域名的，可以直接在Host那里写具体Host。


### 第二步：手机端配置PC的代理

1.在手机的WIFI设置里，修改网络，手动添加代理。

![2019-03-08-使用charles抓取手机https请求包_图片5.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%875.png)

代理服务器主机名：使用PC的本机IP地址

代理服务器端口：使用Charles设置的Port值，Charles按照下图方式配置Port

![2019-03-08-使用charles抓取手机https请求包_图片6.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%876.png)


2.第一次配置完代理，需要在PC端进行允许操作，详见下图的Allow（如果不小心关了下面的弹框，可以重新配置一下手机代理或在Charles里手动添加）

![2019-03-08-使用charles抓取手机https请求包_图片7.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%877.png)

Charles里添加允许访问的IP的方法：

![2019-03-08-使用charles抓取手机https请求包_图片8.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%878.png)

![2019-03-08-使用charles抓取手机https请求包_图片9.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%879.png)
 
###第三步：PC端Charles安装https证书

Help->SSL Proxying ->Install Charles Root Certificate，然后在钥匙串中信任证书即可

![2019-03-08-使用charles抓取手机https请求包_图片10.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8710.png)
![2019-03-08-使用charles抓取手机https请求包_图片11.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8711.png)


### 第四步：手机端下载Charles的证书
 
根据Help->SSL Proxying ->Install Charles Root Certificate on Mobile Device or Remote Browser...获得下载证书的地址，操作如下图：

![2019-03-08-使用charles抓取手机https请求包_图片12.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8712.png)

手机浏览器打开网址下载证书：http://charlesproxy.com/getssl
 
安装证书即可，特殊机型说明如下：

1.小米安装比较特殊，需要在设置->其他高级设置->安全和隐私->凭据存储->从存储设备安装->选择下载的证书安装

2.ios10以上系统，需要在设置->通用->关于本机，信任安装的证书

![2019-03-08-使用charles抓取手机https请求包_图片13.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8713.png)

然后就可以抓包了

![2019-03-08-使用charles抓取手机https请求包_图片14.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8714.png)

抓取包注意事项：如果要抓取Safari等浏览器的包，必须勾选Proxy->macOS Proxy，否则没进行抓包

![2019-03-08-使用charles抓取手机https请求包_图片15.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-03-08-%E4%BD%BF%E7%94%A8charles%E6%8A%93%E5%8F%96%E6%89%8B%E6%9C%BAhttps%E8%AF%B7%E6%B1%82%E5%8C%85_%E5%9B%BE%E7%89%8715.png)






