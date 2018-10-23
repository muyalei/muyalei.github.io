
---
layout:     post
title:      chromedriver版本过低导致selenium驱动chrome失败
subtitle:   selenium
date:       2018-04-19
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - js加密
    - selenium
    - requestium
---

### 错误示例
![2018-04-19-chromedriver版本过低导致selenium驱动chrome失败截图_chromedriver版本报错.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-04-19-chromedriver%E7%89%88%E6%9C%AC%E8%BF%87%E4%BD%8E%E5%AF%BC%E8%87%B4selenium%E9%A9%B1%E5%8A%A8chrome%E5%A4%B1%E8%B4%A5%E6%88%AA%E5%9B%BE_chromedriver%E7%89%88%E6%9C%AC%E6%8A%A5%E9%94%99.png)

### 解决方法
1.更新chromedriver版本

各chromedriver版本镜像[下载地址](http://npm.taobao.org/mirrors/chromedriver/)

2.设置环境变量

将chromedriver所在目录添加进用户环境变量的Path下，如下图所示：
![2018-04-19-chromedriver版本过低导致selenium驱动chrome失败截图_chromedriver添加进环境变零.jpg](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-04-19-chromedriver%E7%89%88%E6%9C%AC%E8%BF%87%E4%BD%8E%E5%AF%BC%E8%87%B4selenium%E9%A9%B1%E5%8A%A8chrome%E5%A4%B1%E8%B4%A5%E6%88%AA%E5%9B%BE_chromedriver%E6%B7%BB%E5%8A%A0%E8%BF%9B%E7%8E%AF%E5%A2%83%E5%8F%98%E9%9B%B6.jpg)


