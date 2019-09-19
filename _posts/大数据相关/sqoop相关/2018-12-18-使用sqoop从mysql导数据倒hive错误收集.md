---
layout: default 
author: muaylei
date: 2018-12-18
title: 使用sqoop从mysql导数据到hive错误收集
tags:
   - sqoop相关
---

***当前环境 hadoop2.8.3+hive2.3.4+sqoop1.4.7***

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

4、错误信息：

   `ERROR sqoop.Sqoop: Got exception running Sqoop: java.lang.RuntimeException: Could not load db driver class: com.mysql.jdbc.Driver`

   解决方法：
   
   将hive/lib目录下的 mysql-connector-java-"版本号"-bin.jar 复制到 sqoop/lib目录下。

   *参考[https://blog.csdn.net/qq_35732963/article/details/56009705](https://blog.csdn.net/qq_35732963/article/details/56009705)*

5、sqoop分隔符问题<br/>
   在将mysql 中的数据导入到hive中，mysql 中的数据如下:<br/>
   ![2018-12-21-sqoop使用_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-12-21-sqoop%E4%BD%BF%E7%94%A8_%E5%9B%BE%E7%89%871.png)
 
   XH=1在mysql中这是一条数据，但是数据对应的某一列数据有换行符。<br/>
   在进行sqoop import 数据时，如果不加其他参数，导入的数据默认的列分隔符是’\001’，默认的行分隔符是’\n’。也就像下面的数据那样，在导入时出现换行符时hive以为 这条数据已经结束，并将其后面输入的数据当做另一条数据。<br/> 
   因而hive 默认会解析成两条数据，这样就造成导入数据时出现了数据跟原表不一致的问题。如下图所示：<br/>
   ![2018-12-21-sqoop使用_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-12-21-sqoop%E4%BD%BF%E7%94%A8_%E5%9B%BE%E7%89%872.png)
   
   解决方法：<br/>
   加上参数–hive-drop-import-delims来把导入数据中包含的hive默认的分隔符去掉 <br/>
