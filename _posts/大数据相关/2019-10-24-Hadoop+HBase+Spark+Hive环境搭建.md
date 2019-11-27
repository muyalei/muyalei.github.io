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

# 1. Windows下安装Ubuntu双系统
Hadoop等大数据开源框架是不支持Windows系统的，所以需要先安装一个Linux双系统。当然，如果你有一台单独的电脑用来安装Ubuntu系统，就不需要安装双系统了。

双系统安装

请参考安装指南：

第一步：[制定系统启动U盘](https://links.jianshu.com/go?to=https%3A%2F%2Fjingyan.baidu.com%2Farticle%2F0f5fb099ef132c6d8234ea5e.html)

第二步：[安装双系统](https://links.jianshu.com/go?to=https%3A%2F%2Fjingyan.baidu.com%2Farticle%2Fdca1fa6fa3b905f1a44052bd.html)


# 2.搭建Hadoop平台

Hadoop是Apache 公司开发的一款可靠的、可扩展性的、分布式计算的开源软件。以Hadoop分布式文件系统（HDFS）和分布式运算编程框架（MapReduce）为核心，允许在集群服务器上使用简单的编程模型对大数据集进行分布式处理。下面，请跟着作者一步步搭建自己的Hadoop平台吧。作者：杨赟快跑
链接：https://www.jianshu.com/p/a4a0e7e4e4b7

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

Java环境推荐使用 Oracle 的 JDK，首先，准备好文件[jdk-8u162-linux-x64.tar.gz](https://pan.baidu.com/s/1jPbN3DjIzV0Ln3UFS9a1tw)(密码:q67c)，然后将文件移到/usr/local目录下：

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

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-10-24-Hadoop%2BHBase%2BSpark%2BHive%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA_%E5%9B%BE%E7%89%87_1.png)

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

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-10-24-Hadoop%2BHBase%2BSpark%2BHive%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA_%E5%9B%BE%E7%89%87_2.png)

成功启动后，可以访问 Web 界面 http://localhost:50070 查看 NameNode 和 Datanode 信息，还可以在线查看 HDFS 中的文件。


## 2.6 Hadoop配置（集群模式）

###2.6.1 设置静态IP（以主节点为例）

编辑文件/etc/network/interfaces

```
vim /etc/network/interfaces
```

在文件后面添加如下配置信息（eth0是网卡名，需要根据实际情况更改）

```
auto eth0 #网卡名
iface eth0 inet static
address 192.168.1.2 #静态IP（可根据实际情况自由设置）
netmask 255.255.255.0 #子网掩码
gateway 192.168.1.1 #网关
dns-nameservers 192.168.1.1 #DNS服务器地址，与网关相同即可
```

编辑文件/etc/resolve.conf

```
vim /etc/resolve.conf
```

在文件中添加如下配置信息

```
nameserver 192.168.1.1
```

此dns在系统重启后会失效，编辑文件/etc/resolvconf/resolv.conf.d/base

```
vim /etc/resolvconf/resolv.conf.d/base
```

添加如下内容，从而永久保存DNS配置

```
nameserver 192.168.1.1
```

运行如下命令重启网络

```
/etc/init.d/networking restart
```

如果重启后无效，则重启系统。

重启后如果发现找不到网卡，则启用系统托管网卡

```
vim /etc/NetworkManager/NetworkManager.conf
```

修改

```
managed=false
```

为

```
managed=true
```

运行如下命令重启网络

```
/etc/init.d/networking restart
```

如果重启后无效，则重启系统。

### 2.6.2 配置hosts文件(每台主机都要配置)

修改主机名

```
vim /etc/hostname
```

提示：主节点设置为master，从节点设置为slave1、slave2等等。

编辑文件/etc/hosts

```
vim /etc/hosts
```

将以下数据复制进入集群的各个主机中

```
192.168.1.2     master
192.168.1.11    slave1
```

注意：若再增加一个从机，则添加slave2的信息

使用以下指令在master主机中进行测试，可使用类似指令在slave1上测试：

```
ping slave1
```

如果ping的通，说明网络连接正常，否则请检查网络连接或者IP信息是否正确。

### 2.6.3 SSH无密码登陆节点（master上配置）

这个操作是要让 master 节点可以无密码 SSH 登陆到各个 slave 节点上。

首先生成 master 节点的公匙，在 master节点的终端中执行（因为改过主机名，所以还需要删掉原有的再重新生成一次）：

```
cd ~/.ssh               # 如果没有该目录，先执行一次ssh localhost
rm ./id_rsa*            # 删除之前生成的公匙（如果有）
ssh-keygen -t rsa       # 一直按回车就可以
```

让 master 节点需能无密码 SSH 本机，在 master 节点上执行：

```
cat ./id_rsa.pub >> ./authorized_keys
```

完成后可执行 ssh master 验证一下（可能需要输入 yes，成功后执行 exit 返回原来的终端）。接着在 master 节点将上公匙传输到 slave1节点：

```
scp ~/.ssh/id_rsa.pub root@slave1:/root/
```

scp 是 secure copy 的简写，用于在 Linux 下进行远程拷贝文件，类似于 cp 命令，不过 cp 只能在本机中拷贝。执行 scp 时会要求输入 slave1 上 root 用户的密码。

接着在 slave1 节点上，将 ssh 公匙加入授权

```
mkdir /root/.ssh       # 如果不存在该文件夹需先创建，若已存在则忽略
cat /root/id_rsa.pub >> /root/.ssh/authorized_keys
rm /root/id_rsa.pub    # 用完就可以删掉了
```

如果有其他 slave 节点，也要执行将 master 公匙传输到 slave 节点、在 slave 节点上加入授权这两步。

这样，在 master 节点上就可以无密码 SSH 到各个 slave 节点了，可在 master 节点上执行如下命令进行检验：

```
ssh root@slave1
```

如果不需要密码，则配置成功。

### 2.6.4 修改Hadoop配置文件（master上配置）

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
        <value>hdfs://master:9000</value>
    </property>
</configuration>
```

同样的，修改配置文件 hdfs-site.xml(gedit /usr/local/hadoop/etc/hadoop/hdfs-site.xml)：

```
<configuration>
        <property>
                <name>dfs.namenode.secondary.http-address</name>
                <value>Master:50090</value>
        </property>
        <property>
                <name>dfs.replication</name>
                <value>2</value>
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

修改文件 mapred-site.xml （可能需要先重命名，默认文件名为 mapred-site.xml.template），然后配置修改如下：

```
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
        <property>
                <name>mapreduce.jobhistory.address</name>
                <value>master:10020</value>
        </property>
        <property>
                <name>mapreduce.jobhistory.webapp.address</name>
                <value>master:19888</value>
        </property>
</configuration>
```

配置yarn-site.xml(gedit /usr/local/hadoop/etc/hadoop/yarn-site.xml)

```
<configuration>
<property>
     <name>yarn.resourcemanager.hostname</name>
     <value>master</value>
</property>
<property>
     <name>yarn.nodemanager.resource.memory-mb</name>
     <value>10240</value>
</property>
<property>
     <name>yarn.nodemanager.aux-services</name>
     <value>mapreduce_shuffle</value>
</property>
</configuration>
```

修改文件 hadoop-env.sh (gedit /usr/local/hadoop/etc/hadoop/hadoop-env.sh)，在文件开始处添加Hadoop和Java环境变量。

```
export JAVA_HOME=/usr/local/java
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:/usr/local/hadoop/bin
```

配置slaves(gedit /usr/local/hadoop/etc/hadoop/slaves)，删除默认的localhost，增加从节点:

```
slave1
```

注意：若再增加一个从机，再添加slave2

配置好后，将 master 上的 /usr/local/hadoop 文件夹复制到各个节点上。

```
sudo rm -rf /usr/local/hadoop/tmp     # 删除 Hadoop 临时文件
sudo rm -rf /usr/local/hadoop/logs   # 删除日志文件
scp -r /usr/local/hadoop slave1:/usr/local
```

注意：每台从机上需要配置Hadoop的环境变量

在master节点上启动hadoop

```
/usr/local/hadoop/bin/hdfs namenode -format
/usr/local/hadoop/sbin/start-all.sh
```

成功启动后，运行jps命令

```
source /etc/profile
jps
```

如果安装成功，master节点会有NameNode进程，slave节点会有DataNode进程。

成功启动后，可以访问 Web 界面 http://master:50070 查看 NameNode 和 Datanode 信息，还可以在线查看 HDFS 中的文件。


# 3.安装HBase数据库

HBase是一个分布式的、面向列的开源数据库,源于Google的一篇论文《BigTable：一个结构化数据的分布式存储系统》。HBase以表的形式存储数据，表有行和列组成，列划分为若干个列族/列簇(column family)。欲了解HBase的官方资讯，请访问HBase官方网站。HBase的运行有三种模式：单机模式、伪分布式模式、分布式模式。
单机模式：在一台计算机上安装和使用HBase，不涉及数据的分布式存储；伪分布式模式：在一台计算机上模拟一个小的集群；分布式模式：使用多台计算机实现物理意义上的分布式存储。这里出于学习目的，我们只重点讨论伪分布式模式。

## 3.1HBase安装

下载 hbase-2.0.0-bin.tar.gz 文件，并将文件移到/usr/local目录下

```
mv hbase-2.0.0-bin.tar.gz /usr/local
```

解压

```
tar -zxvf hbase-2.0.0-bin.tar.gz
```

文件夹重命名

```
mv hbase-2.0.0 hbase
```

将hbase下的bin目录添加到path中，这样，启动hbase就无需到/usr/local/hbase目录下，大大的方便了hbase的使用。教程下面的部分还是切换到了/usr/local/hbase目录操作，有助于初学者理解运行过程，熟练之后可以不必切换。

编辑/etc/profile文件

```
vim /etc/profile
```

在/etc/profile文件尾行添加如下内容：

```
export HBASE_HOME=/usr/local/hbase
export PATH=$HBASE_HOME/bin:$PATH
export HBASE_MANAGES_ZK=true
```

编辑完成后，按 esc 退出编辑模式，然后输入:+wq ，按回车保存（也可以按shift + zz 进行保存），最后再执行source命令使上述配置在当前终端立即生效，命令如下：

```
source /etc/profile
```

查看HBase版本，确定hbase安装成功,命令如下：

```
hbase version
```

## 3.2HBase伪分布模式配置

配置/usr/local/hbase/conf/hbase-site.xml，打开并编辑hbase-site.xml，命令如下：

```
gedit /usr/local/hbase/conf/hbase-site.xml
```

在启动HBase前需要设置属性hbase.rootdir，用于指定HBase数据的存储位置，因为如果不设置的话，hbase.rootdir默认为/tmp/hbase-${user.name},这意味着每次重启系统都会丢失数据。此处设置为HBase安装目录下的hbase-tmp文件夹即（/usr/local/hbase/hbase-tmp）,添加配置如下：

```
<configuration>
        <property>
                <name>hbase.rootdir</name>
                <value>hdfs://localhost:9000/hbase</value>
        </property>
        <property>
                <name>hbase.cluster.distributed</name>
                <value>true</value>
        </property>
</configuration>
```

打开文件（gedit /usr/local/hbase/conf/hbase-env.sh）添加java环境变量

```
export JAVA_HOME=/usr/local/java
export HBASE_HOME=/usr/local/hbase
export PATH=$PATH:/usr/local/hbase/bin
export HBASE_MANAGES_ZK=true
```

## 3.3 HBase集群模式配置

修改master节点的配置文件hbase-site.xml(gedit /usr/local/hbase/conf/hbase-site.xml)

```
   <configuration>
        <property>
                <name>hbase.rootdir</name>
                <value>hdfs://master:9000/hbase</value>
        </property>
        <property>
                <name>hbase.cluster.distributed</name>
                <value>true</value>
        </property>
        <property>
                <name>hbase.zookeeper.quorum</name>
                <value>master,slave1</value>
        </property>
        <property>
                <name>hbase.temp.dir</name>
                <value>/usr/local/hbase/tmp</value>
        </property>
        <property>
                <name>hbase.zookeeper.property.dataDir</name>
                <value>/usr/local/hbase/tmp/zookeeper</value>
        </property>
        <property>
                <name>hbase.master.info.port</name>
                <value>16010</value>
        </property>
</configuration>
```

注意：若再增加一个从机，hbase.zookeeper.quorum 添加slave2

修改配置文件regionservers(gedit /usr/local/hbase/conf/regionservers)，删除里面的localhosts,改为：

```
master
slave1
```

若再增加一个从机，添加slave2

传送Hbase至其它slave节点(从机不需下载安装包，由主机传送过去即可，从机环境变量需要配置)，即将配置好的hbase文件夹传送到各个节点对应位置上：
```
scp -r /usr/local/hbase root@slave1:/usr/local/
```

注意：每台从机上需要配置HBase的环境变量

## 3.4 HBase集群模式配置（使用外置的zookeeper）

在3.3的基础上，修改/etc/profile、/usr/local/hbase/conf/hbase-env.sh文件的配置

```
export HBASE_MANAGES_ZK=false
```

修改/usr/local/hbase/conf/hbase-site.xml文件的配置，将hbase.zookeeper.quorum属性设置为zookpeer的各个节点

```
<property>
         <name>hbase.zookeeper.quorum</name>
         <value>zk1:2181,zk2:2181,zk3:2181</value>
</property>
```

将/etc/profile和/usr/local/hbase/conf文件夹复制到regionserver节点

```
scp /etc/profile slave1:/etc
scp -r /usr/local/hbase/conf/ slave1:/usr/local/hbase
scp /etc/profile slave2:/etc
scp -r /usr/local/hbase/conf/ slave2:/usr/local/hbase
scp /etc/profile slave3:/etc
scp -r /usr/local/hbase/conf/ slave3:/usr/local/hbase
```

## 3.5 测试运行

首先切换目录至HBase安装目录/usr/local/hbase；再启动HBase。命令如下：

```
/usr/local/hadoop/sbin/start-all.sh  #启动hadoop，如果已启动，则不用执行该命令
/usr/local/hbase/start-hbase.sh     #启动hbase
hbase shell                           #进入hbase shell，如果可以进入说明HBase安装成功了
```

停止HBase运行,命令如下：

```
bin/stop-hbase.sh
```

如果hbase启动成功，则使用jps命令会出现如下进程

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_3.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-10-24-Hadoop%2BHBase%2BSpark%2BHive%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA_%E5%9B%BE%E7%89%87_3.png)

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_4.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-10-24-Hadoop%2BHBase%2BSpark%2BHive%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA_%E5%9B%BE%E7%89%87_4.png)


# 4. 安装Spark内存计算引擎

Apache Spark 是一个新兴的大数据处理通用引擎，提供了分布式的内存抽象。Spark 最大的特点就是快，可比 Hadoop MapReduce 的处理速度快 100 倍。Spark基于Hadoop环境，Hadoop YARN为Spark提供资源调度框架，Hadoop HDFS为Spark提供底层的分布式文件存储。

## 4.1. Spark安装

Spark的安装过程较为简单，在已安装好 Hadoop 的前提下，经过简单配置即可使用，首先下载 spark-2.3.0-bin-hadoop2.7.tgz 文件，并将文件移到/usr/local目录下

```
mv spark-2.3.0-bin-hadoop2.7.tgz /usr/local
```

解压

```
cd /usr/local
tar -zxvf spark-2.3.0-bin-hadoop2.7.tgz
```

文件夹重命名

```
mv spark-2.3.0 spark
```

编辑/etc/profile文件，添加环境变量

```
vim /etc/profile
```

在/etc/profile文件尾行添加如下内容：

```
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

编辑完成后，保存退出，再执行source命令使上述配置在当前终端立即生效，命令如下：

```
source /etc/profile
```

## 4.2. Spark单机配置

配置文件spark-env.sh

```
cd /usr/local/spark
cp ./conf/spark-env.sh.template ./conf/spark-env.sh
```

编辑spark-env.sh文件(vim ./conf/spark-env.sh)，在第一行添加以下配置信息:

```
export JAVA_HOME=/usr/local/java
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
export HADOOP_HDFS_HOME=/usr/local/hadoop
export SPARK_HOME=/usr/local/spark
export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
SPARK_MASTER_WEBUI_PORT=8079
```

## 4.3. Spark集群配置

在master上配置文件spark-env.sh

```
cd /usr/local/spark
cp ./conf/spark-env.sh.template ./conf/spark-env.sh
```

编辑spark-env.sh文件(vim ./conf/spark-env.sh)，在第一行添加以下配置信息:

```
export JAVA_HOME=/usr/local/java
export SCALA_HOME=/usr/local/scala
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
export HADOOP_HDFS_HOME=/usr/local/hadoop
export SPARK_HOME=/usr/local/spark
export SPARK_MASTER_IP=master
export SPARK_MASTER_PORT=7077
export SPARK_MASTER_HOST=master
export SPARK_WORKER_CORES=2
export SPARK_WORKER_PORT=8901
export SPARK_WORKER_INSTANCES=1
export SPARK_WORKER_MEMORY=2g
export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
export SPARK_MASTER_WEBUI_PORT=8079
```

保存并刷新配置：

```
source spark-env.sh
```

配置从机列表：

```
cp slaves.template slaves
gedit slaves
```

在最后加上：

```
master
slave1
```

把主机的spark文件夹复制到从机，复制脚本如下：

```
scp -r /usr/local/spark root@slave1:/usr/local
```

注意：每台从机上需要配置Spark的环境变量

## 4.4 验证Spark安装和配置

通过运行Spark自带的示例，验证Spark是否安装成功。

```
cd /usr/local/spark
./sbin/start-all.sh
bin/run-example SparkPi 2>&1 | grep "Pi is"
```

运行结果如下图所示，可以得到π 的 14位小数近似值：

![2019-10-24-Hadoop+HBase+Spark+Hive环境搭建_图片_5.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2019-10-24-Hadoop%2BHBase%2BSpark%2BHive%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA_%E5%9B%BE%E7%89%87_5.png)

在主机的浏览器输入http://master:8079（集群模式）或者http://localhost:8079(单机模式)就可以看到有两个节点在spark集群上。

# 5. 安装hive

Hive是一个架构在Hadoop之上的数据仓库基础工具，用来处理结构化数据，为大数据查询和分析提供方便。最初，Hive是由Facebook开发，后来由Apache软件基金会开发，并作为进一步将它作为名义下Apache Hive为一个开源项目。Hive 不是一个关系数据库，也不是一个设计用于联机事务处（OLTP）实时查询和行级更新的语言。简单的说，Hive就是在Hadoop上架了一层SQL接口，可以将SQL翻译成MapReduce去Hadoop上执行，这样就使得数据开发和分析人员很方便的使用SQL来完成海量数据的统计和分析，而不必使用编程语言开发MapReduce那么麻烦。

## 5.1. Hive安装

下载 apache-hive-1.2.2-bin.tar.gz 文件，并将文件移到/usr/local目录下

```
mv apache-hive-1.2.2-bin.tar.gz /usr/local
```

解压

```
tar -zxvf apache-hive-1.2.2-bin.tar.gz
```

文件夹重命名

```
mv apache-hive-1.2.2 hive
```

编辑/etc/profile文件，配置环境变量

```
vim /etc/profile
```

在/etc/profile文件尾行添加如下内容：

```
export HIVE_HOME=/usr/local/hive
export PATH=$PATH:$HIVE_HOME/bin
```

编辑完成后，保存退出，再执行source命令使上述配置在当前终端立即生效，命令如下：

```
source /etc/profile
```

## 5.2. 安装并配置MySQL

我们采用MySQL数据库保存Hive的元数据，而不是采用Hive自带的derby来存储元数据。ubuntu下Mysql的安装比较简单，直接运行如下命令。在安装过程中，会要求配置用户名和密码，这个一定要记住。

```
apt-get install mysql-server
```

启动并登陆mysql shell

```
service mysql start
mysql -u root -p  #登陆shell界面
```

新建hive数据库

```
#这个hive数据库与hive-site.xml中localhost:3306/hive的hive对应，用来保存hive元数据
mysql> create database hive; 
```

将hive数据库的字符编码设置为latin1（重要）

```
mysql> alter database hive character set latin1;
```

## 5.3. Hive配置

修改/usr/local/hive/conf下的hive-site.xml，执行如下命令：

```
cd /usr/local/hive/conf
mv hive-default.xml.template hive-default.xml
```

上面命令是将hive-default.xml.template重命名为hive-default.xml，然后，使用vim编辑器新建一个配置文件hive-site.xml，命令如下：

```
cd /usr/local/hive/conf
vim hive-site.xml
```

在hive-site.xml中添加如下配置信息，其中：USERNAME和PASSWORD是MySQL的用户名和密码。

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true</value>
    <description>JDBC connect string for a JDBC metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
    <description>Driver class name for a JDBC metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>USERNAME</value>
    <description>username to use against metastore database</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>PASSWORD</value>
    <description>password to use against metastore database</description>
  </property>
</configuration>
```

然后，按键盘上的“ESC”键退出vim编辑状态，再输入:wq，保存并退出vim编辑器。由于Hive在连接MySQL时需要JDBC驱动，所以首先需要下载对应版本的驱动，然后将驱动移动到/usr/local/hive/lib中。

注：我是用了centos7+mariadb，用的jdbc驱动程序是:[https://pan.baidu.com/disk/home#/all?path=%2F%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3_%E5%AE%89%E8%A3%85%E5%8C%85&vmode=list](https://pan.baidu.com/disk/home#/all?path=%2F%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3_%E5%AE%89%E8%A3%85%E5%8C%85&vmode=list)

```
#解压
tar -zxvf mysql-connector-java-5.1.47.tar.gz
#将mysql-connector-java-5.1.47.tar.gz拷贝到/usr/local/hive/lib目录下
cp mysql-connector-java-5.1.47/mysql-connector-java-5.1.47-bin.jar /usr/local/hive/lib
```

启动hive（启动hive之前，请先启动hadoop集群）。

```
./usr/local/hadoop/sbin/start-all.sh #启动hadoop，如果已经启动，则不用执行该命令
hive  #启动hive
```

## 5.4. Spark和Hive的整合

Hive的计算引擎默认为MapReduce，如果想要用Spark作为Hive的计算引擎，可以参考文章编译Spark源码支持Hive并部署


# 6. 报错整理

* 6.1 错误信息："ECDSA host key for ip has changed"或者"Host key verification failed."
  
  解决方法：[https://github.com/muyalei/muyalei.github.io/blob/gh-pages/_posts/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3/2019-10-24-ssh%E7%99%BB%E5%BD%95%E6%88%96%E8%80%85%E5%90%AF%E5%8A%A8hadoop%E3%80%81hbase%E6%97%B6%E6%8A%A5%E9%94%99ECDSA%20host%20key%20for%20ip%20has%20changed%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95.md](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/_posts/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3/2019-10-24-ssh%E7%99%BB%E5%BD%95%E6%88%96%E8%80%85%E5%90%AF%E5%8A%A8hadoop%E3%80%81hbase%E6%97%B6%E6%8A%A5%E9%94%99ECDSA%20host%20key%20for%20ip%20has%20changed%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95.md)

* 6.2 错误信息：Hive在spark2.0.0启动时 "无法访问../lib/spark-assembly-\*.jar: 没有那个文件或目录的解决办法"

  解决方法：[https://github.com/muyalei/muyalei.github.io/blob/gh-pages/_posts/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3/2019-10-24-Hive%E5%9C%A8spark2.0.0%E5%90%AF%E5%8A%A8%E6%97%B6%E6%8A%A5%E9%94%99%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AEspark-assembly-*.jar:%E6%B2%A1%E6%9C%89%E9%82%A3%E4%B8%AA%E6%96%87%E4%BB%B6%E6%88%96%E7%9B%AE%E5%BD%95%E7%9A%84%E8%A7%A3%E5%86%B3%E5%8A%9E%E6%B3%95.md](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/_posts/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%9B%B8%E5%85%B3/2019-10-24-Hive%E5%9C%A8spark2.0.0%E5%90%AF%E5%8A%A8%E6%97%B6%E6%8A%A5%E9%94%99%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AEspark-assembly-*.jar:%E6%B2%A1%E6%9C%89%E9%82%A3%E4%B8%AA%E6%96%87%E4%BB%B6%E6%88%96%E7%9B%AE%E5%BD%95%E7%9A%84%E8%A7%A3%E5%86%B3%E5%8A%9E%E6%B3%95.md)




