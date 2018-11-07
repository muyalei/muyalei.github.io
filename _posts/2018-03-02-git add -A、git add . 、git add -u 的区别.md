---
layout: default
author: muyalei
date: 2018-03-02
title: git add -A、git add . 、git add -u的区别
tags:
   - git
---

转载自[https://www.cnblogs.com/skura23/p/5859243.html](https://www.cnblogs.com/skura23/p/5859243.html)

git add -A和 git add .   git add -u在功能上看似很相近，但还是存在一点差别

git add . ：他会监控工作区的状态树，使用它会把工作时的所有变化提交到暂存区，包括文件内容修改(modified)以及新文件(new)，但不包括被删除的文件。

git add -u ：他仅监控已经被add的文件（即tracked file），他会将被修改的文件提交到暂存区。add -u 不会提交新文件（untracked file）。（git add --update的缩写）

git add -A ：是上面两个功能的合集（git add --all的缩写）

下面是具体操作例子，方便更好的理解（Git version 1.x）：
```
git init
echo Change me > change-me
echo Delete me > delete-me
git add change-me delete-me
git commit -m initial

echo OK >> change-me
rm delete-me
echo Add me > add-me

git status
# Changed but not updated:
#   modified:   change-me
#   deleted:    delete-me
# Untracked files:
#   add-me

git add .
git status

# Changes to be committed:
#   new file:   add-me
#   modified:   change-me
# Changed but not updated:
#   deleted:    delete-me

git reset

git add -u
git status

# Changes to be committed:
#   modified:   change-me
#   deleted:    delete-me
# Untracked files:
#   add-me

git reset

git add -A
git status

# Changes to be committed:
#   new file:   add-me
#   modified:   change-me
#   deleted:    delete-me
```
#### 总结：

- git add -A  提交所有变化

- git add -u  提交被修改(modified)和被删除(deleted)文件，不包括新文件(new)

- git add .  提交新文件(new)和被修改(modified)文件，不包括被删除(deleted)文件

git版本不同会有所区别：

Git Version 1.x: 
![2018-03-02-git add -A、git add . 、git add -u 的区别_图片1.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-03-02-git%20add%20-A、git%20add%20.%20、git%20add%20-u%20的区别_图片1.jpg)

Git Version 2.x: 
![2018-03-02-git add -A、git add . 、git add -u 的区别_图片2.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-03-02-git%20add%20-A、git%20add%20.%20、git%20add%20-u%20的区别_图片2.jpg)
