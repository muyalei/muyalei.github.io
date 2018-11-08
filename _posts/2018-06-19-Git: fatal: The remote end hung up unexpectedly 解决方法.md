---
layout: default
author: muyalei
date: 2018-06-19
title: Git: fatal: The remote end hung up unexpectedly 解决方法
tags:
   - git
---

转载自[https://blog.csdn.net/oshuangyue12/article/details/78882151](https://blog.csdn.net/oshuangyue12/article/details/78882151)

```
git config --global http.postBuffer 524288000
 
# some comments below report having to double the value:
git config --global http.postBuffer 1048576000
```
