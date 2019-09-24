---
layout: default
author: muyalei 
title: "Exception: Python in worker has different version 2.7 than that in driver 3.6, ..."
date: 2019-09-24
tags:
    - pyspark相关
---

***整理自[https://blog.csdn.net/weixin_40136018/article/details/84001276](https://blog.csdn.net/weixin_40136018/article/details/84001276)***

### 一、错误产生

***错误产生描述：***

使用`pip3 install pyspark`安装pyspark后，使用时报标题中错误信息：

***报错完整信息：*** 

Exception: Python in worker has different version 2.7 than that in driver 3.6, PySpark cannot run with different minor versions.Please check environment variables PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON are correctly set.

### 二、解决方法

***方式1***

1、修改~/.bash_profile文件，增加下列行：
```
#更改系统默认python版本为python3
alias python="/usr/local/bin/python3"
#声明pyspark的相关变量
export PYSPARK_PYTHON=/usr/local/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3
```

2、修改的环境变量立即生效：`source .bash_profile`

***方式2***

在py代码中import os修改环境变量
```
import os
 
PYSPARK_PYTHON = /home/piting/ENV/anaconda3/bin/python
os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
```







