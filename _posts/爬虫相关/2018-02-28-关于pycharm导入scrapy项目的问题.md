---
layout:     post
title:      关于pycharm导入scrapy项目的问题
subtitle:   
date:       2018-02-28
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - scrapy
---

转自[http://blog.csdn.net/Haihao_micro/article/details/78529370](http://blog.csdn.net/Haihao_micro/article/details/78529370)

1.导入包的问题，如下面的情况，我想把scrapy目录下的items.py里面的Class导入时出现的问题。 
##### 项目目录 
![2018-02-28-关于pycharm导入scrapy项目的问题1.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%981.jpg)

##### items.py 
![2018-02-28-关于pycharm导入scrapy项目的问题2.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%982.jpg)

##### 问题
![2018-02-28-关于pycharm导入scrapy项目的问题3.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%983.jpg)

### 解决办法 
第一步：项目文件下右键*Make Directory as–Source Root* 

![2018-02-28-关于pycharm导入scrapy项目的问题4.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%984.jpg)
这样子可以保证<br> 
*from items import WebcrawlerScrapyItem* <br>
在项目中没有错误。<br> 
但是，实际上命令行运行scrapy crawl 时还是会报NO Moudle name “items”的问题<br>

第二步： 
将*from items import WebcrawlerScrapyItem*改为<br> 
*from ..items import WebcrawlerScrapyItem*

“..”表示在上一级目录下找 <br>
最终的效果如下： 

![2018-02-28-关于pycharm导入scrapy项目的问题5.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%985.jpg)

第三步：<br> 
1、运行scrapy crawl [爬虫名称] 命令，就没问题了<br> 
2、最近遇到的问题，在二级目录下运行一个.py文件，但是用”..”和 Mark as Source Root 等方法都没有用，这是python3.0以上出现的问题，可以采用以下的办法解决：</br> 
假设我要运行下面的pictureSpider_demo.py文件 

![2018-02-28-关于pycharm导入scrapy项目的问题6.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-02-28-%E5%85%B3%E4%BA%8Epycharm%E5%AF%BC%E5%85%A5scrapy%E9%A1%B9%E7%9B%AE%E7%9A%84%E9%97%AE%E9%A2%986.jpg)

请在命令行下的执行 <br>
*python -m webCrawler_scrapy.spiders.pictureSpider_demo.py* 
这样就行了，否则还是会报*pakage out of top level*这样的错误

还有一个很有效的办法就是：<br> 
在需要彼此获取相关类的两个.py文件分别加入以下<>

import sys
sys.path.append("..")
```
import sys
sys.path.append("..")
```
然后就没问题了
