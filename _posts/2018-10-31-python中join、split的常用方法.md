---
layout: default
author: muyalei
date: 2018-10-31
title: python中join、split的常用方法
tags:
   - python笔记
---


python join 和 split方法的使用,join用来连接字符串，split恰好相反，拆分字符串的。

1.join用法示例 
```
li = ['my','name','is','bob'] 
' '.join(li) 
'my name is bob' 
 
'_'.join(li) 
'my_name_is_bob' 
 
s = ['my','name','is','bob'] 
 ' '.join(s) 
'my name is bob' 
 
'..'.join(s) 
'my..name..is..bob' 
``` 
2.split用法示例 
```
b = 'my..name..is..bob' 
 
b.split() 
['my..name..is..bob'] 
 
b.split("..") 
['my', 'name', 'is', 'bob'] 
 
b.split("..",0) 
['my..name..is..bob'] 
 
b.split("..",1) 
['my', 'name..is..bob'] 
 
b.split("..",2) 
['my', 'name', 'is..bob'] 
 
b.split("..",-1) 
['my', 'name', 'is', 'bob'] 
``` 
可以看出b.split("..",-1)等价于b.split("..") 
