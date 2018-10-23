---
layout:     post
title:      pyton中random模块的使用
subtitle:   python模块
date:       2018-02-11
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - python模块
---

## #python random使用方法
如果你对在Python生成随机数与random模块中最常用的几个函数的关系与不懂之处，下面的文章就是对Python生成随机数与random模块中最常用的几个函数的关系，希望你会有所收获，以下就是这篇文章的介绍。  

## #random.random()
用于生成一个指定范围内的随机符点数，两个参数其中一个是上限，一个是下限。如果a > b，则生成随机数```n: a <= n <= b。如果 a <b， 则 b <= n <= a```
## #random.uniform()  
>print random.uniform(10, 20)    
print random.uniform(20, 10)     
18.7356606526     
12.5798298022     

## #random.randint
>用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，Python生成随机数  
print random.randint(12, 20) #生成的随机数n: 12 <= n <= 20   
print random.randint(20, 20) #结果永远是20    
#print random.randint(20, 10) #该语句是错误的。  
下限必须小于上限。  

## #random.randrange
>从指定范围内，按指定基数递增的集合中 ，这篇文章就是对python生成随机数的应用程序的部分介绍。  
随机整数：  
import random  
random.randint(0,99)  
21  
#例如  
随机选取0到100间的偶数：  
import random  
random.randrange(0, 101, 2)  
42  

## #random.choice
>随机字符：  
random.choice('abcdefg&#%^*f')  
'd'  
随机选取字符串：  
import random  
random.choice ( ['apple', 'pear', 'peach', 'orange', 'lemon'] )  
'lemon'  

## #random.sample  
>多个字符中选取特定数量的字符：  
import random  
random.sample('abcdefghij',3)   
['a', 'd', 'b']  

## #random.sample
>多个字符中选取特定数量的字符组成新字符串：  
import random  
import string  
string.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], 3)).r  
eplace(" ","")  
'fih'  

## #random.shuffle()
>洗牌：<br>
items = [1, 2, 3, 4, 5, 6] <br>
random.shuffle(items) <br>
items <br>
[3, 2, 5, 6, 4, 1]<br>

转自[OnTheWay_duking](https://www.cnblogs.com/duking1991/p/6121300.html)
