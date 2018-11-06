---
layout: default
author: muyalei
date: 2018-11-06
title: "hadoop报错：WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicabl”"
tags:
   - hadoop
---

安装Hadoop的时候直接用的bin版本，根据教程安装好之后运行的时候发现出现了：WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable 错误，百度很多都说是版本（32,64）问题，需要重新编译源码，历经一天的时间源码重新编译完成之后，再次运行仍旧有这个错误，google的解决方案是：

1. 执行：` export HADOOP_ROOT_LOGGER=DEBUG,console`

查看具体的错误信息：
```
17/03/16 11:35:47 DEBUG util.Shell: setsid exited with exit code 0
17/03/16 11:35:47 DEBUG conf.Configuration: parsing URL jar:file:/usr/local/hadoop/share/hadoop/common/hadoop-common-2.7.1.jar!/core-default.xml
17/03/16 11:35:47 DEBUG conf.Configuration: parsing input stream sun.net.www.protocol.jar.JarURLConnection$JarURLInputStream@462ac22a
17/03/16 11:35:47 DEBUG conf.Configuration: parsing URL file:/usr/local/hadoop/etc/hadoop/core-site.xml
17/03/16 11:35:47 DEBUG conf.Configuration: parsing input stream java.io.BufferedInputStream@405a2273
17/03/16 11:35:48 DEBUG lib.MutableMetricsFactory: field org.apache.hadoop.metrics2.lib.MutableRate org.apache.hadoop.security.UserGroupInformation$UgiMetrics.loginSuccess with annotation @org.apache.eName=Time, value=[Rate of successful kerberos logins and latency (milliseconds)], about=, always=false, type=DEFAULT, sampleName=Ops)
17/03/16 11:35:48 DEBUG lib.MutableMetricsFactory: field org.apache.hadoop.metrics2.lib.MutableRate org.apache.hadoop.security.UserGroupInformation$UgiMetrics.loginFailure with annotation @org.apache.eName=Time, value=[Rate of failed kerberos logins and latency (milliseconds)], about=, always=false, type=DEFAULT, sampleName=Ops)
17/03/16 11:35:48 DEBUG lib.MutableMetricsFactory: field org.apache.hadoop.metrics2.lib.MutableRate org.apache.hadoop.security.UserGroupInformation$UgiMetrics.getGroups with annotation @org.apache.hadme=Time, value=[GetGroups], about=, always=false, type=DEFAULT, sampleName=Ops)
17/03/16 11:35:48 DEBUG impl.MetricsSystemImpl: UgiMetrics, User and group related metrics
17/03/16 11:35:48 DEBUG util.KerberosName: Kerberos krb5 configuration not found, setting default realm to empty
17/03/16 11:35:48 DEBUG security.Groups:  Creating new Groups object
17/03/16 11:35:48 DEBUG util.NativeCodeLoader: Trying to load the custom-built native-hadoop library...
17/03/16 11:35:48 DEBUG util.NativeCodeLoader: Failed to load native-hadoop with error: java.lang.UnsatisfiedLinkError: no hadoop in java.library.path
17/03/16 11:35:48 DEBUG util.NativeCodeLoader: java.library.path=/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib
17/03/16 11:35:48 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/03/16 11:35:48 DEBUG util.PerformanceAdvisory: Falling back to shell based
17/03/16 11:35:48 DEBUG security.JniBasedUnixGroupsMappingWithFallback: Group mapping impl=org.apache.hadoop.security.ShellBasedUnixGroupsMapping
17/03/16 11:35:48 DEBUG security.Groups: Group mapping impl=org.apache.hadoop.security.JniBasedUnixGroupsMappingWithFallback; cacheTimeout=300000; warningDeltaMs=5000
17/03/16 11:35:48 DEBUG security.UserGroupInformation: hadoop login
17/03/16 11:35:48 DEBUG security.UserGroupInformation: hadoop login commit
17/03/16 11:35:48 DEBUG security.UserGroupInformation: using local user:UnixPrincipal: hadoop
17/03/16 11:35:48 DEBUG security.UserGroupInformation: Using user: "UnixPrincipal: hadoop" with name hadoop
17/03/16 11:35:48 DEBUG security.UserGroupInformation: User entry: "hadoop"
17/03/16 11:35:48 DEBUG security.UserGroupInformation: UGI loginUser:hadoop (auth:SIMPLE)
```
其中有个warn信息，在这个信息附近找到一个：Failed to load native-hadoop with error: java.lang.UnsatisfiedLinkError，这表明是java.library.path出了问题，

解决方案是在文件hadoop-env.sh中增加：

export HADOOP_OPTS="-Djava.library.path=${HADOOP_HOME}/lib/native"  

解决问题过程中遇到的比较好的链接：

[http://blog.csdn.net/l1028386804/article/details/51538611](http://blog.csdn.net/l1028386804/article/details/51538611)

[http://blog.csdn.net/xichenguan/article/details/38797331](http://blog.csdn.net/xichenguan/article/details/38797331)

[http://www.chinahadoop.cn/classroom/5/thread/43](http://www.chinahadoop.cn/classroom/5/thread/43)

[http://www.powerxing.com/install-hadoop-in-centos/](http://www.powerxing.com/install-hadoop-in-centos/)


