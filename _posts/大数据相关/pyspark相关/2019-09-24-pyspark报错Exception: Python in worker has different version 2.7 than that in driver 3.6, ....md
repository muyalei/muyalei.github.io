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

### 三、另一种报这个错误信息的情况

***整理自[https://www.jianshu.com/p/4169ff63a65d](https://www.jianshu.com/p/4169ff63a65d)***

运行py文件
```
spark-submit --master spark://node1:7077  
/home/shexiaobin/spark/examples/src/main/python/pi.py   100
```
出现了以下的报错：
```
Exception: Python in worker has different version 2.7 than that in driver 3.7, PySpark cannot run with different minor versions.Please check environment variables PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON are correctly set.

    at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:330)
    at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:470)
    at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:453)
    at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:284)
    at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
    at scala.collection.Iterator$GroupedIterator.fill(Iterator.scala:1126)
    at scala.collection.Iterator$GroupedIterator.hasNext(Iterator.scala:1132)
    at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:408)
    at org.apache.spark.shuffle.sort.BypassMergeSortShuffleWriter.write(BypassMergeSortShuffleWriter.java:125)
    at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:96)
    at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:53)
    at org.apache.spark.scheduler.Task.run(Task.scala:109)
    at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:345)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
    at java.lang.Thread.run(Thread.java:748)
```
解决方法：

设置PYSPARK_PYTHON
```
cd   /home/shexiaobin/spark/conf
vi spark-env.sh
# 加入以下内容
export PYSPARK_PYTHON=/home/shexiaobin/anaconda3/bin/python
```




