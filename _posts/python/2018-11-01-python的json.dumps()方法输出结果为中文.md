---
layout: default
author: muyalei
date: 2018-11-01
title: python的json.dumps\(\)方法输出为中文
tags:
   - python笔记
---

python的json.dumps方法默认会输出成这种格式"\u535a\u5ba2\u56ed",。

要输出中文需要指定ensure_ascii参数为False，如下代码片段：

json.dumps({'text':"中文"},ensure_ascii=False,indent=2)
