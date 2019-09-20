---
layout: default
author: muyalei 
title: python中的enumerate函数
date: 2019-09-20
tags:
    - python相关
---

***整理自(https://www.cnblogs.com/Ray-Lei/p/9681535.html)[https://www.cnblogs.com/Ray-Lei/p/9681535.html]***

写这个笔记的时候，突然想到今天20号了，发工资啊～～

Python的enumerate函数是一个神话般的存在，以至于它很难用一句话去总结它的目的和用处。

但是，它是一个非常有用的函数，许多初学者，甚至中级Pythonistas是并没有真正意识到。简单来说，enumerate()是用来遍历一个可迭代容器中的元素，同时通过一个计数器变量记录当前元素所对应的索引值。

示例：
```
names = ['Bob', 'Alice', 'Guido']
for index, value in enumerate(names):
    print(f'{index}: {value}')
输出：
0 Bob
1 Alice
2 Guido 
``` 
 
另一个有用的特性是，enumerate()函数允许我们为循环自定义起始索引值。

enumerate()函数中接受一个可选参数，该参数允许你为本次循环中的计数器变量设置初始值。

示例：
```
names = ['Bob', 'Alice', 'Guido']
for index, value in enumerate(names,5):
    print(f'{index}: {value}')
输出：
5 Bob
6 Alice
7 Guido 
```
在上面的例子中，函数调用改为enumerate(names,5)，后面的参数5就是本次循环的起始索引，替换默认的0
