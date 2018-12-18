---
layout: default 
author: muaylei
date: 2018-12-18
title: 使用sqoop从mysql导数据到hive错误收集
tags:
   - sqoop相关
---


1、错误信息：

  `main ERROR Could not register mbeans java.security.AccessControlException: access denied ("javax.management.MBeanTrustPermission" "register")`
  
   解决方法：

   ```
   #vim $JAVA_HOME/jre/lib/security/java.policy
   在grant{}内部添加如下内容：
   permission javax.management.MBeanTrustPermission "register";
   ```
   亲测上述方法可用。

   不过，也有人测试上述方法无效，使用方法 "将hive-site.xml复制到${SQOOP_HOME}/conf" 解决该问题，详细参考[https://blog.csdn.net/weixin_39445556/article/details/80802459](https://blog.csdn.net/weixin_39445556/article/details/80802459)


   注意：不要通过前缀 # 添加注释信息！！跟python中不一样，{...}中前缀#并代表注释，添加会报错！！千万不要自找麻烦！！

2、错误信息：

  `java.lang.NoSuchMethodError: com.fasterxml.jackson.databind.ObjectMapper.readerFor(Ljava/lang/Class;)Lcom/fasterxml/jackson/databind/ObjectReader;`

   解决方法：

   将`$SQOOP_HOME/lib/jackson*.jar` 文件bak，再把`$HIVE_HOME/lib/jackson*.jar` 拷贝至 `$SQOOP_HOME/lib` 目录中，重新运行sqoop 作业，导入成功。
  
   *参考自[https://blog.csdn.net/qq_34117327/article/details/80395704](https://blog.csdn.net/qq_34117327/article/details/80395704)*

3、错误信息：

  `java.lang.Exception: java.lang.RuntimeException: java.lang.ClassNotFoundException: Class widgets not found`

   错误原因：

   因为在使用sqoop import命令时，生成的java文件会默认产生在当前目录下，而产生的.jar文件和.class文件会默认存放在/tmp/sqoop-/compile下，两者不在同一文件目录下，导致错误。所以，我们需要将java文件，.jar文件和.class文件放在同一目录下。
   
   解决方法：

   增加 `--bindir ./` 参数

   *参考自[java.lang.ClassNotFoundException](java.lang.ClassNotFoundException)*

