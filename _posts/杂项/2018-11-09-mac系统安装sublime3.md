---
layout: default
author: muyalei
date: 2018-11-09
title: mac系统安装sublime3
tags:
   - mac使用
---

***转载自[https://blog.csdn.net/oppo62258801/article/details/81212861](https://blog.csdn.net/oppo62258801/article/details/81212861)***

不管是Linux操作系统还是mac操作系统，sublime都是程序员们钟爱的IDE。下面总结一下自己在Mac安装sublime的过程。

现在可用sublime3，下面我也以sublime3的下载安装过程为例。

首先需要下载sublime安装包，下载链接 [http://www.sublimetext.com/3](http://www.sublimetext.com/3)（备用下载链接：[https://github.com/muyalei/muyalei.github.io/blob/gh-pages/tools/Sublime%20Text%20Build%203176.dmg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/tools/Sublime%20Text%20Build%203176.dmg)），链接进去后界面如下所示，点击红框中链接即可下载安装包，将安装包保存到电脑相应位置即可。

![2018-11-09-mac系统安装sublime3_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%871.png)

安装包名称为 Sublime Text Build 3176.dmg，而对于mac中的*.dmg文件，直接双击在界面安装打开即可，打开如下。

![2018-11-09-mac系统安装sublime3_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%872.png)_

接下来是在安装及初始化部分比较重要的内容，按control+`来显示如图3所示的界面，在红色框中输入相应的代码，代码见链接[https://packagecontrol.io/installation#st3](https://packagecontrol.io/installation#st3) 中，如图4中红色比分的代码。

![2018-11-09-mac系统安装sublime3_图片3.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%873.png)
![2018-11-09-mac系统安装sublime3_图片4.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%874.png)
```
#预防代码丢失，贴在此处
import urllib.request,os,hashlib; h = '6f4c264a24d933ce70df5dedcf1dcaee' + 'ebe013ee18cced0ef93d5f746d80ef60'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```

填完之后回车即可，安装完成以后重启sublime3，就能查看到如下图5的界面了

![2018-11-09-mac系统安装sublime3_图片5.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%875.png)

最后就是安装插件的事了，command+shift+p，即可显示如下图6所示的界面，在框中输入install package，下面会出现相应的候选列表，选择第一个回车即可，然后会显示正在另外一个框如图7所示，在框里面输入自己想要安装的任何插件就可以安装了。

![2018-11-09-mac系统安装sublime3_图片6.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%876.png)
![2018-11-09-mac系统安装sublime3_图片7.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-09-mac%E7%B3%BB%E7%BB%9F%E5%AE%89%E8%A3%85sublime3_%E5%9B%BE%E7%89%877.png)

常用的可以的安装插件如下：

ChineseLocalizations：一种让sublime汉化的插件

Colorpicker：使用一个取色器改变颜色

Emmet（原名 Zen Coding）：一种快速编写html/css的方法
