---
layout: default
author: muyalei
date: 2018-03-03
title: git commit -m 与 git commit -am 的区别
tags:
   - git
---

当修改已经通过git add <change file>将其添加到stage，可以通过git commit -m "<message>"为这所有已经进入stage的改变添加一个commit信息。什么是在stage中？看下面

![2018-03-03-git commit -m 与git commit -am的区别_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-03-03-git%20commit%20-m%20与git%20commit%20-am的区别_图片1.png)

如果你的文件之前已经提交过，但这次的改动还没有进stage，如下：

![2018-03-03-git commit -m 与git commit -am的区别_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-03-03-git%20commit%20-m%20与git%20commit%20-am的区别_图片2.png)

可以直接使用git commit -am "<message>"，将所有修改，但未进stage的改动加入stage，并记录commit信息。(某种程度上相当于git add和git commit -m的组合技，前提是被改动文件已经是tracked)
