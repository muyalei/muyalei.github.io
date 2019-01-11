---
layout: default 
author: muyalei
date: 2019-01-11
title: mac安装chromedriver及配置
tags:
   - selenium
---


***整理自[https://blog.csdn.net/ywj_486/article/details/80940087](https://blog.csdn.net/ywj_486/article/details/80940087)***


各版本chromedriver下载地址：[http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)

chromedriver与chrome浏览器版本对应关系：
```
chromedriver版本	支持的Chrome版本<br/>
v2.41	            v67-69<br/>  
v2.40	            v66-68<br/>  
v2.39	            v66-68<br/>  
v2.38	            v65-67<br/>  
v2.37	            v64-66<br/>  
v2.36	            v63-65<br/>  
v2.35	            v62-64<br/>  
v2.34	            v61-63<br/>  
v2.33	            v60-62<br/>  
v2.32	            v59-61<br/>  
v2.31	            v58-60<br/>  
v2.30	            v58-60<br/>  
v2.29	            v56-58<br/>  
v2.28	            v55-57<br/>  
v2.27	            v54-56<br/>  
v2.26	            v53-55<br/>  
v2.25	            v53-55<br/>  
v2.24	            v52-54<br/>  
v2.23	            v51-53<br/>  
v2.22	            v49-52<br/>  
v2.21	            v46-50<br/>  
v2.20	            v43-48<br/>  
v2.19	            v43-47<br/>  
v2.18	            v43-46<br/>  
v2.17	            v42-43<br/>  
v2.13	            v42-45<br/>  
v2.15	            v40-43<br/>  
v2.14	            v39-42<br/>  
v2.13	            v38-41<br/>  
v2.12	            v36-40<br/>  
v2.11	            v36-40<br/>  
v2.10	            v33-36<br/>  
v2.9	            v31-34<br/>  
v2.8	            v30-33<br/>  
v2.7	            v30-33<br/>  
v2.6	            v29-32<br/>  
v2.5	            v29-32<br/>  
v2.4	            v29-32<br/>  
```

将下载的chromedriver移动到/usr/local/bin目录下，解压，chromedriver --version检查版本。<br/>
将chromedriver添加进环境变量：<br/>
export PATH=$PATH:/usr/local/bin/ChromeDriver










