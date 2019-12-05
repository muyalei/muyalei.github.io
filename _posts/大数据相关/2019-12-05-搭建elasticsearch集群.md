---
layout: default
author: muyalei
title: 搭建elasticsearch集群+安装kibana
date: 2019-12-05
tags:
    - 大数据
---

***整理自[https://cloud.tencent.com/developer/article/1189282](https://cloud.tencent.com/developer/article/1189282)***

### 安装 Elasticsearch

接下来我们来安装 Elasticsearch，同样是每台主机都需要安装。

首先需要添加 Apt-Key：
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```
然后添加 Elasticsearch 的 Repository 定义：
```
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
```
接下来安装 Elasticsearch 即可：
```
sudo apt-get update 
sudo apt-get install elasticsearch
```
运行完毕之后我们就完成了 Elasticsearch 的安装，注意还是要每台主机都要安装。

### 配置 Elasticsearch

这时我们只是每台主机都安装好了 Elasticsearch，接下来我们还需要将它们联系在一起构成一个集群。

安装完之后，Elasticsearch 的配置文件是 /etc/elasticsearch/elasticsearch.yml，接下来让我们编辑一下配置文件：

- 集群的名称

通过 cluster.name 可以配置集群的名称，集群是一个整体，因此名称都要一致，所有主机都配置成相同的名称，配置示例：
```
cluster.name: germey-es-clusters
```

- 节点的名称

通过 node.name 可以配置每个节点的名称，每个节点都是集群的一部分，每个节点名称都不要相同，可以按照顺序编号，配置示例：
```
node.name: es-node-1
```

其他的主机可以配置为 es-node-2、es-node-3 等。

- 是否有资格成为主节点

通过 node.master 可以配置该节点是否有资格成为主节点，如果配置为 true，则主机有资格成为主节点，配置为 false 则主机就不会成为主节点，可以去当数据节点或负载均衡节点。注意这里是有资格成为主节点，不是一定会成为主节点，主节点需要集群经过选举产生。这里我配置所有主机都可以成为主节点，因此都配置为 true，配置示例：
```
node.master: true
```

- 是否是数据节点

通过 node.data 可以配置该节点是否为数据节点，如果配置为 true，则主机就会作为数据节点，注意主节点也可以作为数据节点，当 node.master 和 node.data 均为 false，则该主机会作为负载均衡节点。这里我配置所有主机都是数据节点，因此都配置为 true，配置示例：
```
node.data: true
```

- 数据和日志路径

通过 path.data 和 path.logs 可以配置 Elasticsearch 的数据存储路径和日志存储路径，可以指定任意位置，这里我指定存储到 1T 硬盘对应的路径下，另外注意一下写入权限问题，配置示例：
```
path.data: /datadrive/elasticsearch/data
path.logs: /datadrive/elasticsearch/logs
```

- 设置访问的地址和端口

我们需要设定 Elasticsearch 运行绑定的 Host，默认是无法公开访问的，如果设置为主机的公网 IP 或 0.0.0.0 就是可以公开访问的，这里我们可以都设置为公开访问或者部分主机公开访问，如果是公开访问就配置为：
```
network.host: 0.0.0.0
```
如果不想被公开访问就不用配置。

另外还可以配置访问的端口，默认是 9200：
```
http.port: 9200
```

- 集群地址设置

通过 discovery.zen.ping.unicast.hosts 可以配置集群的主机地址，配置之后集群的主机之间可以自动发现，这里我配置的是内网地址，配置示例：
```
discovery.zen.ping.unicast.hosts: ["10.0.0.4", "10.0.0.5", "10.0.0.6", "10.0.0.7", "10.0.0.8", "10.0.0.9", "10.0.0.10"]
```
这里请改成你的主机对应的 IP 地址。

- 节点数目相关配置

为了防止集群发生“脑裂”，即一个集群分裂成多个，通常需要配置集群最少主节点数目，通常为 (可成为主节点的主机数目 / 2) + 1，例如我这边可以成为主节点的主机数目为 7，那么结果就是 4，配置示例：
```
discovery.zen.minimum_master_nodes: 4
```
另外还可以配置当最少几个节点回复之后，集群就正常工作，这里我设置为 4，可以酌情修改，配置示例：
```
gateway.recover_after_nodes: 4
```
其他的暂时先不需要配置，保存即可。注意每台主机都需要配置。

- 启动 Elasticsearch

配置完成之后就可以在每台主机上分别启动 Elasticsearch 服务了，命令如下：
```
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```
所有主机都启动之后，我们在任意主机上就可以查看到集群状态了，命令行如下：
```
curl -XGET 'http://localhost:9200/_cluster/state?pretty'
```
类似的输出如下：
```
{
    "cluster_name": "germey-es-clusters",
    "compressed_size_in_bytes": 20799,
    "version": 658,
    "state_uuid": "a64wCwPnSueKRtVuKx8xRw",
    "master_node": "73BQvOC2TpSXcr-IXBcDdg",
    "blocks": {},
    "nodes": {
        "I2M80AP-T7yVP_AZPA0bpA": {
            "name": "es-node-1",
            "ephemeral_id": "KpCG4jNvTUGKNHNwKKoMrA",
            "transport_address": "10.0.0.4:9300",
            "attributes": {
                "ml.machine_memory": "7308464128",
                "ml.max_open_jobs": "20",
                "xpack.installed": "true",
                "ml.enabled": "true"
            }
        },
        "73BQvOC2TpSXcr-IXBcDdg": {
            "name": "es-node-7",
            "ephemeral_id": "Fs9v2XTASnGbqrM8g7IhAQ",
            "transport_address": "10.0.0.10:9300",
            "attributes": {
                "ml.machine_memory": "14695202816",
                "ml.max_open_jobs": "20",
                "xpack.installed": "true",
                "ml.enabled": "true"
            }
        },
....
```
可以看到这里输出了集群的相关信息，同时 nodes 字段里面包含了每个节点的详细信息，这样一个基本的集群就构建完成了。

***注意***：ES可以通过`-d`参数指定后台运行、`-p {绝对路径}`参数指定ES的pid文件位置，例如 `./elasticsearch -d -p /usr/local/es`


### 安装kibana

过程参考开头的链接。

***注意***：kibana没有提供后台运行的参数，要后台运行kibana，使用`nohup ./kibana >/dev/null 2>&1 &`
