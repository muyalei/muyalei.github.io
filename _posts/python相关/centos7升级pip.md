---
layout: muyalei
author: muyalei
title: centos7升级pip
date: 2021-09-09
tags:
	- python相关
---


- 遇到问题

执行`pip install --upgrade pip`后pip运行报错`File “/usr/lib/python2.7/site-packages/pip/_internal/cli/main.py”, line 60`

- 解决方法

```
yum remove python-pip
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python get-pip.py
pip -V
```

pip20.3.4版本下载地址：[https://pypi.org/project/pip/20.3.4/#files](https://pypi.org/project/pip/20.3.4/#files)

