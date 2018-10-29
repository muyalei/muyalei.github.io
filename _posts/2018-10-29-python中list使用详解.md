---
layout: default
author: muyalei
date: 2018-10-29
title: python中list使用详解
tags:
   - python笔记
---

转载自[http://www.linuxidc.com/Linux/2012-01/51638.htm](http://www.linuxidc.com/Linux/2012-01/51638.htm)

Python3.2.2列表操作总结

list操作：快速创建list、新增item、删除item、重新赋值item、颠倒item顺序、检索item

快捷创建list，两种方式：split方法、list函数和range函数配合使用。
 

* split方法。写一个字符串，字符之间以空格分隔，然后对该字符串使用split方法。
a_list = 'a b c d e f g'.spit()  //创建列表['a','b','c','d','e','f','g']，但这种写法要简洁很多

* list函数和range函数配合使用。可以快速地创建一个非常大的列表。
a_list = list(range(100))   //很方便地创建一个0到99的列表

 

* 新增item，四种方式：concatenation、append、extend、insert，后三种方式都是列表的方法。
示例列表a_list = ['a']：
concatenation添加。它添加的是另外一个列表，两个列表组合成一个新的列表： 
a_list = a_list + [2.0,3]  //列表较长时，可能会消耗大量内存

* append方法添加。它在原列表末尾添加一个item，item类型可以是任意的：
a_list.append('hello')  //在原有列表末尾添加一个类型为字符串的item
a_list.append(['hello'])   //在原有列表末尾添加一个类型为列表的item

* extend方法添加。它类似于concatenation，只接受列表参数，并把列表中的item分解，然后添加到原有的列表：
a_list.extend('hello')  //在原有列表末尾添加5个字符item，因为它把hello视为列表
a_list.extend(['hello'])  //在原有列表末尾添加1个item

* insert方法添加。在原有列表中插入item：
a_list.insert(0,'c')   //在原有列表的0位置添加一个字符
a_list.insert(0.['c'])   //在原有列表的0位置添加一个列表


* 删除item，三种方式：del、remove、pop，后两种方式都是列表的方法。
示例列表：a_list = ['a','b','c','hello']：
del删除。它按item的索引值或切片进行删除：
del a_list[0]   //删除列表的第一个值
del a_list[:2]   //删除列表的前两个值。（为什么不是前三个呢？因为python的列表切片，包含前一个索引，但不包括后一个索引）

* remove方法删除。它不按item索引，而是按照item的值进行删除：
a_list.remove('a')  //把a从列表中删除

* pop方法删除。它按item索引值进行删除，同时返回被删除的item值；若不指定索引，默认删除最后一个item：
a_list.pop(1)  //删除列表的第二个值，并返回被删除的值
a_list.pop()   //删除列表的最后一个值，并返回被删除的值


* 重新赋值item，对指定索引使用assignment符号进行赋值：
示例列表：a_list = ['a','b','c','hello']：
a_list[1] = 'bbb' //列表的第二个值b，将被替换为bbb


* 颠倒列表的item顺序，reverse方法：
示例列表：a_list = ['a','b','c','hello']：
a_list.reverse()  //列表的item顺序将被从后到前重新排列，更改为['hello','c','b','a']


* 检索列表的值，四种方式：in、not in、count、index，后两种方式是列表的方法。
示例列表：a_list = ['a','b','c','hello']：
判断值是否在列表中，in操作符：
'a' in a_list  //判断值a是否在列表中，并返回True或False

* 判断值是否不在列表，not in操作符：
'a' not in a_list   //判断a是否不在列表中，并返回True或False

* 统计指定值在列表中出现的次数，count方法：
a_list.count('a')  //返回a在列表中的出现的次数

* 查看指定值在列表中的位置，index方法：
a_list.index('a')   //返回a在列表中每一次出现的位置，默认搜索整个列表
a_list.index('a',0,3)  //返回a在指定切片内第一次出现的位置

