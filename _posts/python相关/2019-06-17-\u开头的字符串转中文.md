---
layout: default
author: muyalei
date: 2019-06-17
title: "\\u"开头的字符串转中文
tags: 
   - python相关
---



***整理自[https://www.cnblogs.com/hahaxzy9500/p/7685955.html](https://www.cnblogs.com/hahaxzy9500/p/7685955.html)***


爬虫直接抓取到的内容如下：<br/>

![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-06-17-%5Cu%E5%BC%80%E5%A4%B4%E7%9A%84%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E4%B8%AD%E6%96%87__%E5%9B%BE%E7%89%871.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-06-17-%5Cu%E5%BC%80%E5%A4%B4%E7%9A%84%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E4%B8%AD%E6%96%87__%E5%9B%BE%E7%89%871.png)

直接print出来结果如下：

![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-06-17-%5Cu%E5%BC%80%E5%A4%B4%E7%9A%84%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E4%B8%AD%E6%96%87__%E5%9B%BE%E7%89%872.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-06-17-%5Cu%E5%BC%80%E5%A4%B4%E7%9A%84%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E4%B8%AD%E6%96%87__%E5%9B%BE%E7%89%872.png)

python3的解决办法：字符串.encode('utf-8').decode('unicode_escape')

python2：字符串.decode('unicode_escape')

