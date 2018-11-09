---
layout: default
author: muyalei
date: 2018-05-18
title: "运行Django项目报错：Invalid HTTP_HOST header: '192.168.1.111:8000'. You may need to add '192.168.1.111' to ALLOWED_HOSTS"
tags:
   - Django
---

***转载自[http://www.mamicode.com/info-detail-1978434.html](http://www.mamicode.com/info-detail-1978434.html)***


报错信息如下：

Request Method:	GET

Request URL:	http://202.201.38.70:8000/angular

Django Version:	1.11.3

Exception Type:	DisallowedHost

Exception Value:`Invalid HTTP_HOST header: ‘202.201.38.70:8000‘. You may need to add ‘202.201.38.70‘ to ALLOWED_HOSTS.`

Exception Location:	/usr/local/python3/lib/python3.6/site-packages/Django-1.11.3-py3.6.egg/django/http/request.py in get_host, line 113

Python Executable:	/usr/local/python3/bin/python3

Python Version:	3.6.1

Python Path:
```
[‘/var/www/html/application/mysite‘,
 ‘/usr/local/python3/lib/python36.zip‘,
 ‘/usr/local/python3/lib/python3.6‘,
 ‘/usr/local/python3/lib/python3.6/lib-dynload‘,
 ‘/usr/local/python3/lib/python3.6/site-packages‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/Django-1.11.3-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/pytz-2017.2-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/PyMySQL-0.7.11-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/django_tokenapi-1.0-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/xlrd-1.0.0-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/python_dateutil-2.6.1-py3.6.egg‘,
 ‘/usr/local/python3/lib/python3.6/site-packages/six-1.10.0-py3.6.egg‘]
```
Server time:	Tue, 29 Aug 2017 09:56:31 +0000
运行项目时，输入命令#Python manage.py runserver 192.168.1.111:8000，在本机的浏览器中输入http://192.168.1.111:8000

在我们创建的项目里修改setting.py文件

ALLOWED_HOSTS = [‘\*‘]  ＃在这里请求的host添加了*
