---
layout: default
author: muyalei
date: 2018-10-31
title: python中的open函数
tags:
   - python笔记
---

转载自[https://www.jb51.net/article/80302.htm](https://www.jb51.net/article/80302.htm)

### 一、open()的函数原型
open(file, mode=‘r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
从官方文档中我们可以看到open函数有很多的参数，我们常用的是file，mode和encoding，对于其它的几个参数，平时不常用，也简单介绍一下。
buffering的可取值有0，1， >1三个，0代表buffer关闭（只适用于二进制模式），1代表line buffer（只适用于文本模式），>1表示初始化的buffer大小；
encoding表示的是返回的数据采用何种编码，一般采用utf8或者gbk；
errors的取值一般有strict，ignore，当取strict的时候，字符编码出现问题的时候，会报错，当取ignore的时候，编码出现问题，程序会忽略而过，继续执行下面的程序。
newline可以取的值有None, \n,  \r, '', ‘\r\n' ，用于区分换行符，但是这个参数只对文本模式有效；
closefd的取值，是与传入的文件参数有关，默认情况下为True，传入的file参数为文件的文件名，取值为False的时候，file只能是文件描述符，什么是文件描述符，就是一个非负整数，在Unix内核的系统中，打开一个文件，便会返回一个文件描述符。
### 二、file() 与open()
两者都能够打开文件，对文件进行操作，也具有相似的用法和参数，但是，在我看来，这两种文件打开方式有本质的区别，file为文件类，用file()来打开文件，相当于这是在构造文件类，而用open()打开文件，是用python的内建函数来操作。
### 三、参数Mode的基本取值
![2018-10-31-python中的open函数_图片1.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-python%E4%B8%AD%E7%9A%84open%E5%87%BD%E6%95%B0_%E5%9B%BE%E7%89%871.jpg)

r、w、a为打开文件的基本模式，对应着只读、只写、追加模式；
b、t、+、U这四个字符，与以上的文件打开模式组合使用，二进制模式，文本模式，读写模式、通用换行符，根据实际情况组合使用、


### 四、 常见的mode取值组合
1、r或rt    默认模式，文本模式读
2、rb      二进制文件
3、w或wt    文本模式写，打开前文件存储被清空
4、wb    二进制写，文件存储同样被清空 
5、a   追加模式，只能写在文件末尾
6、a+  可读写模式，写只能写在文件末尾 
7、w+ 可读写，与a+的区别是要清空文件内容
8、r+   可读写，与a+的区别是可以写到文件任何位置 

### 五、几个模式的区别
为了测试不同模式的区别，我们用一小段代码来测试写入文件中的直观不同。
```
test = [ "test1\n", "test2\n", "test3\n" ]
  f = open( "b.txt", "a+")
  try:
    for s in test:
      f.write( s )
  finally:
    f.close()
```
（1）a+与w+模式的区别

![2018-10-31-python中的open方法_图片2.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-python%E4%B8%AD%E7%9A%84open%E5%87%BD%E6%95%B0_%E5%9B%BE%E7%89%872.jpg)

（2）a+与r+模式

![2018-10-31-python中的open方法_图片3.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-python%E4%B8%AD%E7%9A%84open%E5%87%BD%E6%95%B0_%E5%9B%BE%E7%89%873.jpg)

在写入文件前，我们在上面那段代码中加上一句 seek（6），用来定位写入文件写入位置。

注意：r+模式打开文件时，此文件必须存在，否则就会报错，‘r'模式也如此
### 六、换行符带来的烦恼
当你用二进制模式将带有换行符的字符串写入txt文件时，数据存储是正确的，但是当用windows平台的记事本程序打开时，你看到的换行符确实一个个的小黑块，但是，用文本模式，就不存在这样的问题。
在这里，涉及到了不同平台由于编码的问题，而对换行符有不同的识别。unix或者linux系统识别\n为换行符的标识，但是windows平台的编码，对\n不予理睬。
但是python自身带有转化功能，用文本模式的时候，你不会看到由于平台不同而造成的换行效果不同，但是，二进制模式的时候，python便不会再去转化，是什么，就写进去什么，此时的换行符，再用文本模式打开，windows下就不识别‘\n'换行符了。

以上就是关于python中open函数使用方法的相关介绍，希望对大家的学习有所帮助。

