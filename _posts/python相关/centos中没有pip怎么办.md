---
layout: default
author: muyalei
title: centos中没有pip怎么办
date: 2021-09-09
tags:
	- 操作系统相关
---

1. 查看是否安装依赖包，没安装先安装

yum install epel-release

2. 更新文件库

yum -y update

3. 安装pip

yum -y install python-pip