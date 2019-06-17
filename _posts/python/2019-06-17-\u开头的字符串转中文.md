---
layout: default
author: muyalei
title: "\u"开头的字符串转中文
tag: 
   - python相关
---



***整理自[https://www.cnblogs.com/hahaxzy9500/p/7685955.html](https://www.cnblogs.com/hahaxzy9500/p/7685955.html)***


爬虫直接抓取到的内容如下：<br/>
![]()

直接print出来结果如下：
![]()

python3的解决办法：字符串.encode('utf-8').decode('unicode_escape')

python2：字符串.decode('unicode_escape')

