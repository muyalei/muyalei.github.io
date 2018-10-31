---
layout: default
author: muyalei
date: 2018-10-31
titile: \r,\n,\r\n的区别
tags:
   - python笔记
---

代码：
```
string s1 = "已经习惯了回车和换行一次搞定\n，敲一个回车键，即是回";   
Console.WriteLine(s1);
s1 = "已经习惯了回车和换行一次搞定\r，敲一个回车键，即是回";
Console.WriteLine(s1);
s1 = "已经习惯了回车和换行一次搞定\r\n，敲一个回车键，即是回";
Console.WriteLine(s1);
Console.ReadLine();
```
结果：

![2018-10-31-\r,\n,\r\n的区别_图片1.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-%5Cr%2C%5Cn%2C%5Cr%5Cn%E7%9A%84%E5%8C%BA%E5%88%AB_%E5%9B%BE%E7%89%871.jpg)
#### 回车、换行的区别  
他们间的区别其实是个回车换行的问题

先来段历史

回车”（Carriage Return）和“换行”（Line Feed）这两个概念的来历和区别。

符号        ASCII码        意义

\n               10          换行

\r                13            回车CR

在计算机还没有出现之前，有一种叫做电传打字机（Teletype Model 33，Linux/Unix下的tty概念也来自于此）的玩意，每秒钟可以打10个字符。但是它有一个问题，就是打完一行换行的时候，要用去0.2秒，正好可以打两个字符。要是在这0.2秒里面，又有新的字符传过来，那么这个字符将丢失。

于是，研制人员想了个办法解决这个问题，就是在每行后面加两个表示结束的字符。一个叫做“回车”，告诉打字机把打印头定位在左边界；另一个叫做“换行”，告诉打字机把纸向下移一行。这就是“换行”和“回车”的来历，从它们的英语名字上也可以看出一二。

后来，计算机发明了，这两个概念也就被般到了计算机上。那时，存储器很贵，一些科学家认为在每行结尾加两个字符太浪费了，加一个就可以。于是，就出现了分歧。

在Windows中：

'\r' 回车，回到当前行的行首，而不会换到下一行，如果接着输出的话，本行以前的内容会被逐一覆盖；

'\n' 换行，换到当前位置的下一行，而不会回到行首；

Unix系统里，每行结尾只有“<换行>”，即"\n"；Windows系统里面，每行结尾是“<回车><换行>”，即“\r\n”；Mac系统里，每行结尾是“<回车>”，即"\r"；。一个直接后果是，Unix/Mac系统下的文件在Windows里打开的话，所有文字会变成一行；而Windows里的文件在Unix/Mac下打开的话，在每行的结尾可能会多出一个^M符号。

例:

`$ echo -en '12\n34\r56\n\r78\r\n' > tmp.txt`

![2018-10-31-\r,\n,\r\n的区别_图片2.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-%5Cr%2C%5Cn%2C%5Cr%5Cn%E7%9A%84%E5%8C%BA%E5%88%AB_%E5%9B%BE%E7%89%872.jpg)

![2018-10-31-\r,\n,\r\n的区别_图片3.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-10-31-%5Cr%2C%5Cn%2C%5Cr%5Cn%E7%9A%84%E5%8C%BA%E5%88%AB_%E5%9B%BE%E7%89%873.jpg)

分别在Windws和Linux中查看此文件可知:

Linux中遇到换行符("\n")会进行回车+换行的操作，回车符反而只会作为控制字符("^M")显示，不发生回车的操作。而windows中要回车符+换行符("\r\n")才会回车+换行，缺少一个控制符或者顺序不对都不能正确的另起一行。

本质的分析，请参考[C++中回车换行（\n\r）和换行(\r)的区别](https://blog.csdn.net/xiaofei2010/article/details/8458605)

 

注意点：

在解析文本或其他格式的文件内容时，常常要碰到判定回车换行的地方，这个时候就要注意既要判定"\r\n"又要判定"\n"。

写程序时可能得到一行,将其进行trim掉'\r',这样能得到你所需要的string了。
