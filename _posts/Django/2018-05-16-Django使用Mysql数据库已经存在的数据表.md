---
layout: default
author: muaylei
date: 2018-05-16
title: Django使用Mysql数据库已经存在的数据表
tags:
   - Django
---

***转载自[https://blog.csdn.net/liuweiyuxiang/article/details/71155207](https://blog.csdn.net/liuweiyuxiang/article/details/71155207)*** 

使用scrapy爬取了网上的一些数据，存储在了mysql数据库中，想使用Django将数据展示出来，在网上看到都是使用Django的models和makemigration，migrate命令来创建新表，并使用。可是我的数据已经存在了已经创建好，并且已经存储有数据了，不能再重新创建新表了。了解Django的表明和models名称的映射关系就可以让Django使用已经存在的表。

假如在Django存在models如下：
```
from django.db import models
 
# Create your models here.
class Sciencenews(models.Model):
    id = models.CharField(max_length=36,primary_key=True)
    first_module = models.CharField(max_length=30,default="News")
    second_module = models.CharField(max_length=30,default="Latest News")
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=60,null=True)
    publish_date = models.CharField(max_length=35,null=True)
    content = models.TextField(null=True)
    crawl_date = models.CharField(max_length=35,null=True)
    from_url = models.CharField(max_length=350,null=True)
```
执行数据迁移命令：
```
python manage.py makemigration
python manage.py migrate
```

会在数据库中生成名称为show_sciencenews的数据表。show为应用名称，此处我的应用名称为show。可以看到Django创建表的命名规则：应用名_模型名。
我的存储爬取到的数据的表格名称原来为science_news,想要Django使用它，而不是创建新的表，只需要把的它的名称改为：应用名_要与该表映射的models名称，在此处我改为show_sciencenews。然后使用如上的数据迁移命令，这时可能会提示数据表已经存在的错误，不用理会，models已经和数据表映射上了。接下来只需要正常使用models和数据表就可以了。
