---
layout: default
author: muyalei
title: Hadoop+HBase+Spark+Hive环境搭建
date: 2019-10-24
tags:
  - 大数据相关
---


***整理自[https://www.jianshu.com/p/a4a0e7e4e4b7](https://www.jianshu.com/p/a4a0e7e4e4b7)***


摘要：大数据门槛较高，仅仅环境的搭建可能就要耗费我们大量的精力，本文总结了作者是如何搭建大数据环境的（单机版和集群版），希望能帮助学弟学妹们更快地走上大数据学习之路。


# 0.准备安装包

本文所需的系统镜像、大数据软件安装包、开发环境软件安装包等都可以在我的百度云盘中下载。

链接：[系统镜像和各种大数据软件](https://links.jianshu.com/go?to=https%3A%2F%2Fpan.baidu.com%2Fs%2F1yYx8DoW3Sus2USmpzGVG4w)

密码：n2cn
 
自用防丢失地址：[自用防丢失](https://pan.baidu.com/disk/home?#/all?vmode=list&path=%2F%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3_%E5%AE%89%E8%A3%85%E5%8C%85)

# 1.安装centos7
 
与原文不同，我这里是安装了虚拟机，在虚拟机上安装了centos7

# 2.搭建Hadoop平台

## 2.1更新源

在bash终端中运行如下shell指令，设置root用户密码，并切换到root用户

```
#设置root密码
sudo passwd
#切换到root用户
su root
```

更新源

```
apt-get update
```

安装vim编译器

```
apt-get install vim
```

备份原始的官方源

```
cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

删除原始的官方源

```
rm /etc/apt/sources.list
```

运行如下shell命令，重新创建sources.list文件

```
vim /etc/apt/sources.list
```

按 i 进入vim的编辑模式，复制下面的清华源到sources.list文件中，然后按 esc 退出编辑模式，最后输入:+wq ，按回车保存（也可以按shift + zz 进行保存）。

```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ artful-proposed main restricted universe multiverse
```

运行如下shell命令，完成源的更新

```
apt-get update
```

## 2.2 安装SSH、配置SSH无密码登陆

***注意：必须要安装ssh-server，否则无法实现免密登录！！***

Ubuntu 默认已安装了 SSH client，此外还需要安装 SSH server：

```
sudo apt-get install openssh-server
```

安装后，修改sshd_config配置

```
vim /etc/ssh/sshd_config
```

在文件中设置如下属性：（按 / 可以进入搜索模式，按esc退出搜索模式）

```
PubkeyAuthentication yes
PermitRootLogin yes
```

重启ssh服务

```
sudo /etc/init.d/ssh restart
```

重启后，可以使用如下命令登陆本机，但此时需要密码才能登陆：

```
ssh localhost
```

首先退出刚才的 ssh，就回到了我们原先的终端窗口，然后利用 ssh-keygen 生成密钥，并将密钥加入到授权中：

```
exit                           # 退出刚才的 ssh localhost
cd ~/.ssh/                     # 若没有该目录，请先执行一次ssh localhost
ssh-keygen -t rsa              # 会有提示，都按回车就可以
cat ./id_rsa.pub >> ./authorized_keys  # 加入授权
```

在 Linux 系统中，~ 代表的是用户的主文件夹（root用户例外），即 “/home/用户名” 这个目录，如你的用户名为 ubuntu，则 ~ 就代表 “/home/ubuntu/”。 如果是root用户则~代表/root，此外，命令中的 # 后面的文字是注释，只需要输入前面命令即可。

此时再用 ssh localhost 命令，无需输入密码就可以直接登陆了。

## 2.3 安装JAVA环境

Java环境推荐使用 Oracle 的 JDK，首先，准备好文件 jdk-8u162-linux-x64.tar.gz，然后将文件移到/usr/local目录下：

```
mv jdk-8u162-linux-x64.tar.gz /usr/local
```

解压文件

```
tar -zxvf jdk-8u162-linux-x64.tar.gz
```

重命名文件夹为java

```
mv jdk-1.8.0_162 java
```

用vim打开/etc/profile文件（Linux下配置系统环境变量的文件）

```
vim /etc/profile
```

按i进入编辑模式，在文件末尾添加如下JAVA环境变量

```
export JAVA_HOME=/usr/local/java
export JRE_HOME=/usr/local/java/jre
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
```

添加环境变量后，结果如下图所示，按 esc 退出编辑模式，然后输入:+wq ，按回车保存（也可以按shift + zz 进行保存）。

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_1.png]()

最后，需要让该环境变量生效，执行如下代码：

```
source /etc/profile
```

检验JAVA是否安装成功

```
echo $JAVA_HOME     # 检验变量值
java -version
java
javac
```

如果设置正确的话，java -version 会输出 java 的版本信息，java 和 javac 会输出命令的使用指导。


## 2.4 安装Hadoop

下载 hadoop-2.7.6.tar.gz 文件，然后将文件移到/usr/local目录下

```
mv hadoop-2.7.6.tar.gz /usr/local
```

解压

```
tar -zxvf hadoop-2.7.6.tar.gz 
```

文件夹重命名为hadoop

```
mv hadoop-2.7.6 hadoop
```

配置环境变量，打开文件/etc/profile，添加如下Hadoop环境变量

```
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin
```

同样，需要让该环境变量生效，执行如下代码：

```
source /etc/profile
```

输入如下命令来检查 Hadoop 是否可用，成功则会显示 Hadoop 版本信息：

```
hadoop version
```

## 2.5 Hadoop配置（单机伪分布式模式）

Hadoop 可以在单节点上以伪分布式的方式运行，Hadoop 进程以分离的 Java 进程来运行，节点既作为 NameNode 也作为 DataNode，同时，读取的是 HDFS 中的文件。

修改配置文件 core-site.xml (gedit /usr/local/hadoop/etc/hadoop/core-site.xml)，将当中的

```
<configuration>
</configuration>
```

修改为下面配置：

```
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

同样的，修改配置文件 hdfs-site.xml(gedit /usr/local/hadoop/etc/hadoop/hdfs-site.xml)：

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/data</value>
    </property>
</configuration>
```

修改文件 hadoop-env.sh (gedit /usr/local/hadoop/etc/hadoop/hadoop-env.sh)，在文件开始处添加Hadoop和Java环境变量。

```
export JAVA_HOME=/usr/local/java
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:/usr/local/hadoop/bin
```

**Hadoop配置文件说明**

Hadoop 的运行方式是由配置文件决定的（运行 Hadoop 时会读取配置文件），伪分布式只需要配置 fs.defaultFS 和 dfs.replication 就可以运行（官方教程如此），不过若没有配置 hadoop.tmp.dir 参数，则默认使用的临时目录为 /tmp/hadoo-hadoop，而这个目录在重启时有可能被系统清理掉，导致必须重新执行 format 才行。所以我们进行了设置，同时也指定 dfs.namenode.name.dir 和 dfs.datanode.data.dir，否则在接下来的步骤中可能会出错。

配置完成后，执行 NameNode 的格式化:

```
/usr/local/hadoop/bin/hdfs namenode -format
```

启动hadoop

```
./usr/local/hadoop/sbin/start-all.sh
```

成功启动后，运行jps命令

```
source /etc/profile
jps
```

如果安装成功，则会出现如下如下进程

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_1.png]()

成功启动后，可以访问 Web 界面 http://localhost:50070 查看 NameNode 和 Datanode 信息，还可以在线查看 HDFS 中的文件。



