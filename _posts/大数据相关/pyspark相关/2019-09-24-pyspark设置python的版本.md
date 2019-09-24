---
layout: default
author: muyalei 
title: pyspark设置python的版本
date: 2019-09-24
tags:
    - pyspar相关
---


***整理自[https://blog.csdn.net/abc_321a/article/details/82589836](https://blog.csdn.net/abc_321a/article/details/82589836)***


一般情况下，spark内置的python的版本是2的版本，现在我想把python的版本切换成3的版本，步骤如下（前提是所有节点都已经安装好python3）

1.修改spark-env.sh文件，在末尾添加export PYSPARK_PYTHON=/usr/bin/python3

2.把修改后的spark-env.sh分发到其他子节点的spark安装包下的conf目录下

3.修改spark安装包bin目录下的pyspark，修改下图红色方框的位置，将原来PYSPARK_PYTHON=python改成PYSPARK_PYTHON=python3，同样的，其他子节点也都需要修改

![]()

4.重启Spark，启动pyspark,可发现python的版本已切换成3.6.4的版本

![]()









