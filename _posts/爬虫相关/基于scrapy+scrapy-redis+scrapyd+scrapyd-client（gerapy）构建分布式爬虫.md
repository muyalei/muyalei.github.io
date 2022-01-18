---
layout: default
author: muyalei
date: 2021-09-09
tiitle: python3+scrapy+scrapy-redis+scrapyd+scrapyd-client/gerapy构建分布式爬虫
tags:
	- 爬虫相关
---

# **鄙人原创，转载请注明出处**

**整理自：**

[https://juejin.cn/post/6908717173486092302](https://juejin.cn/post/6908717173486092302)

[https://www.jianshu.com/p/5baa1d5eb6d9](https://www.jianshu.com/p/5baa1d5eb6d9)

[https://blog.csdn.net/qq_38044574/article/details/82716839](https://blog.csdn.net/qq_38044574/article/details/82716839)

[https://blog.csdn.net/xc_zhou/article/details/80907047](https://blog.csdn.net/xc_zhou/article/details/80907047)

[https://developer.aliyun.com/article/69897](https://developer.aliyun.com/article/69897)

[https://www.jianshu.com/p/674d90294f9c](https://www.jianshu.com/p/674d90294f9c)

[https://www.cnblogs.com/xiaozhican/p/9303954.html](https://www.cnblogs.com/xiaozhican/p/9303954.html)

[https://www.cnblogs.com/nixingguo/articles/7253200.html](https://www.cnblogs.com/nixingguo/articles/7253200.html)

[https://www.cnblogs.com/heqiuyong/p/10463334.html](https://www.cnblogs.com/heqiuyong/p/10463334.html)


## 安装scrapy、scrapy-redis、scrapyd、scrapyd-client、gerapy

```
pip3 install scrapy
pip3 install scrapy-redis
pip3 install srapyd
pip3 install scrapyd-client
pip3 install gerapy

```
*参考文档：*

[https://scrapy-cookbook.readthedocs.io/zh_CN/latest/scrapy-10.html](https://scrapy-cookbook.readthedocs.io/zh_CN/latest/scrapy-10.html)

[https://scrapyd.readthedocs.io/en/stable/api.html#schedule-json](https://scrapyd.readthedocs.io/en/stable/api.html#schedule-json)

[https://github.com/scrapy/scrapyd-client](https://github.com/scrapy/scrapyd-client)

[https://segmentfault.com/a/1190000020343777](https://segmentfault.com/a/1190000020343777)

## 安装、配置redis

### windows

- **下载地址**

[https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases)

- **安装运行**
   
   - 修改配置文件 
   
   配置文件：安装目录下的`redis.windows-service.conf`

   取消`#bind 127.0.0.1`前的`#`，修改为`bind 0.0.0.0`，即允许其他主机访问

   取消`requirepass xxx`前的`#`，`xxx`为要修改的密码。

   *带密码的redis访问命令：`redis-cli -h x.x.x.x -a xxx -p 6379`*

   - 命令行直接运行

   运行redis服务器：安装目录下的`redis-server.exe`

   运行redis客户端：安装目录下的`redis-cli.exe`

   - 将redis设置为系统服务

   安装服务：`redis-server --service-install redis.windows.conf --loglevel verbose`
   
   启动：`redis-server --service-start`

   可以使用`services.msc`查看服务信息

### linux（centos为例）

- **下载地址**

[http://download.redis.io/releases/](http://download.redis.io/releases/)

- **安装运行**
	
   - 安装

      1. 安装gcc依赖

      `yum install -y gcc`
      
      2. 下载解压安装包

      ```
      wget http://download.redis.io/releases/redis-5.0.3.tar.gz
      tar -xzvf redis-5.0.3.tar.gz
      ```

      3. 编译

      ```
      cd redis-5.0.3
      make && make install PREFIX=/usr/local/redis

      ```

      4. 将redis-cli命令加入PATH

      `ln -s /usr/local/redis/bin/redis-cli /usr/bin/redis-cli`

      5. 将源码目录中的redis.conf复制到redis的安装目录，并修改配置项

      `cp /usr/local/reids-5.0.3/redis.conf /usr/local/redis/bin`

      修改`daemonize no`为`daemonize yes`（不修改则为前台启动），其他改动同windows。

      6. 启动服务

      ```
      cd /usr/local/redis/bin
      ./redis-server
      ```
      
      7. 设为开机启动

         - 添加开机启动服务

         `vi /etc/systemd/system/redis.service`
         ```
         [Unit]
		 Description=redis-server
		 After=network.target

		 [Service]
		 Type=forking
		 ExecStart=/usr/local/redis/bin/redis-server /usr/local/redis/bin/redis.conf
		 PrivateTmp=true

		 [Install]
		 WantedBy=multi-user.target
         ```
         - 设置开机启动
         
         ```
         systemctl daemon-reload
         systemctl start redis.service
         systemctl enable redis.service
         ```

         - 关闭防火墙（看自己情况）
         ```
         systemctl stop firewalld
         systemctl disable firewalld
         ```

## 使用scrapy-redis

- 继承`RedisSpider`

*参考：*

[https://blog.csdn.net/qq_38044574/article/details/82716839](https://blog.csdn.net/qq_38044574/article/details/82716839)

[https://wangxin1248.github.io/python/2018/11/python3-spider-23.html](https://wangxin1248.github.io/python/2018/11/python3-spider-23.html)

```
from scrapy_redis.spiders import RedisSpider
from jd_book_detail.items import JdBookDetailItem

class JdBookDetailWxSpider(RedisSpider):
    name = 'jd_book_detail_wx'
    redis_key = 'jd_book_detail_wx:start_urls'

    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domains = filter(None,domain.split(','))
        super(JdBookDetailWxSpider,self).__init__(*args,**kwargs)

    def parse(self,response):
        item = JdBookDetailItem()
        print('='*20)
        print(response.body.decode('utf-8'))
        print('=' * 20)
        #resp_json = json.loads(response)
        item['resp_json'] = 111
        return item
```
*注意：*

`RedisSpider`类不需要写`allowd_domains`和`start_urls`：

   - scrapy-redis 将从在构造方法 init() 里动态定义爬虫爬取域范围，也可以选择直接写 allowd_domains。
   
   - 必须指定 redis_key，即启动爬虫的命令，参考格式：redis_key = ‘myspider:start_urls’
   
   - 根据指定的格式，start_urls 将在 Master端的 redis-cli 里 lpush 到 Redis数据库里，RedisSpider 将在数据库里获取 start_urls。

- settings.py

```
BOT_NAME = 'jd_book_detail'

SPIDER_MODULES = ['jd_book_detail.spiders']
NEWSPIDER_MODULE = 'jd_book_detail.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd_book_detail (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Host':'api.m.jd.com',
    'Connection':'keep-alive',
    'wqreferer':'http://wq.jd.com/wxapp/pages/item/detail/detail',
    'cookie':'buildtime=20210823;wxapp_type=1;wxapp_version=7.8.230;wxapp_scene=1089;cid=5;visitkey=30674712635351630047332856;gender=1;province=Guangdong;city=Shenzhen;country=China;nickName=%E4%BA%AC%E4%B8%9C%E7%94%A8%E6%88%B7;avatarUrl=https%3A%2F%2Fimg11.360buyimg.com%2Fjdphoto%2Fs120x120_jfs%2Ft1%2F82031%2F9%2F5133%2F19337%2F5d36bcadE9cdb240c%2Fccc58f73b721ec2d.png;wxNickName=%E4%BA%AC%E4%B8%9C%E7%94%A8%E6%88%B7;wxAvatarUrl=https%3A%2F%2Fimg11.360buyimg.com%2Fjdphoto%2Fs120x120_jfs%2Ft1%2F82031%2F9%2F5133%2F19337%2F5d36bcadE9cdb240c%2Fccc58f73b721ec2d.png;__jda=122270672.fe3cb8477a2c0bc855ced58a9ae84eb7.1630047337513.1630047337513.1630047337513.1;network=wifi;__wga=1630048410925.1630047339448.1630047339448.1630047339448.13.1;__jdv=122270672%7Cdirect%7Ct_1000578828_xcx_1089_ltkxl%7Cxcx%7C-%7C1630048410940;PPRD_P=CT.138567.50.79-EA.17078.49.1-LOGID.1630048411038.1904276481;shshshfpa=944d8563-f145-47c6-2eb2-91a62e4dd07f-1630047340;shshshfp=46c7b754b08a04ce1223e58eae64d27a;shshshsID=5cb7b8d9b5d8d2ac7e42a325adace540_6_1630048410697;shshshfpb=oRU7Bl1%2B7MwwtNk3OPqxw3w%3D%3D;hf_time=1630047342685;jdpin=18714301033_p;mcossmd=09276d2c126de29fe0ecc68c10cc5a8d;open_id=oTGnpnFEL7mTe4h_GATRxrkmW2Uo;pin=18714301033_p;pinStatus=0;unionid=oCwKwuH_ThubEWphgBpnab9HUju0;wid=4504129736;wq_uin=4504129736;wq_unionid=oCwKwuH_ThubEWphgBpnab9HUju0;wxapp_openid=oA1P50OltTsDHSsJxAn5pz5A8Syw;skey=zw4487556B9FA62971BB9690C956BD4F25170AD704C8B2304710502DF3271136F29D1900CA4604CEE663F36E65282326A08D201A7106CF92141B26E220944C329288F6C1B3FC7E4FA0EFC38434CF0F5EFC;wq_skey=zw4487556B9FA62971BB9690C956BD4F25170AD704C8B2304710502DF3271136F29D1900CA4604CEE663F36E65282326A08D201A7106CF92141B26E220944C329288F6C1B3FC7E4FA0EFC38434CF0F5EFC;ou=C53639CF36E6E0FE75BAFDF6F53704C94D996074A350D95377CE9C89F4BD9E0EDDF6783AF88AFA489F0C1D78E4F37B03E7C9122F5D750D3BE580A5295F498C37182A7609A6622990AA373102C223AE10;wq_uits=;wq_auth_token=1E8CBBEC9BF8CF6C6B3378280081188D23D9C0BFFFC712274823802E4B3C27CF',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 MMWEBID/9314 MicroMessenger/7.0.22.1820(0x27001636) Process/appbrand0 WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'charset':'utf-8',
    'Accept-Encoding':'gzip,compress,br,deflate',
    'content-type':'application/json',
    'Referer':'https://servicewechat.com/wx91d27dbf599dff74/557/page-frame.html',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jd_book_detail.middlewares.JdBookDetailSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jd_book_detail.middlewares.JdBookDetailDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jd_book_detail.pipelines.JdBookDetailPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#####################################scrapy-redis设置#####################################
#拓展插件，主要是防止空跑问题
#详细请看：https://my.oschina.net/2devil/blog/1631116，或者:https://blog.csdn.net/xc_zhou/article/details/80907047
EXTENSIONS = {
    'jd_book_detail.extensions.RedisSpiderSmartIdleClosedExensions':500,
}

ITEM_PIPELINES = {
    #'newsSpider.pipelines.NewsspiderPipeline': 300,#这个是新建项目自带的
    'scrapy_redis.pipelines.RedisPipeline':400 #这个是需要加上的，通过scrapy-redis自带的pipelines将item存入redis

}
#启用scrapy-redis自带的去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#启用调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#是否在关闭spider的时候保存记录，保存（TRUE）,不保存（False）
SCHEDULER_PERSIST = True
#使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
#REDIS_URL = None #一般可不带
#指定master的redis地址端口，有密码的加上密码
REDIS_HOST = '192.168.175.132'
REDIS_PORT = '6379'
REDIS_PARAMS = {
    'password':'spider',
}

#SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"  # 对保存到redis中的数据进行序列化，默认使用pickle

#SCHEDULER_FLUSH_ON_START = False  # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
# SCHEDULER_IDLE_BEFORE_CLOSE = 10  # 去调度器中获取数据时，如果为空，最多等待时间（最后没数据，未获取到）。
#SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重规则，在redis中保存时对应的key  chouti:dupefilter
#SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'  # 去重规则对应处理的类
#DUPEFILTER_DEBUG = False
#上述的扩展类需要的
MYEXT_ENABLED = True  #开启扩展
IDLE_NUMBER = 10  #配置空闲持续时间单位为10个，一个时间单位为5s

#如果为True，则使用redis的'spop'进行操作。
#因为本次请求每一次带上的都是时间戳，所以就用了lpush
#如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
#REDIS_START_URLS_AS_SET = True
```

- 向指定的`redis_key`中写入起始请求，开启爬虫

   - 使用list   
   ```
   lpush jd_book_detail_wx:start_urls xxx 
   llen jd_book_detail_wx:start_urls
   ```
   - 使用set
   ```
   sadd jd_book_detail_wx:start_urls xxx
   scard jd_book_detail_wx:start_urls
   ```
   - 开启爬虫
   ```
   scrapy crawl jd_book_detail_wx
   ```

## 使用scrapyd+scrapyd-client部署爬虫

1. scrapyd服务开启

进入scrapyd所在目录（笔者是`D:\python3\Lib\site-packages\scrapyd`），修改配置文件`default_scrapyd.conf`，允许其他主机访问
```
bind_address 0.0.0.0
```

2. 修改爬虫目录下文件`scrapy.cfg`
```
[settings]
default = jd_book_detail.settings

[deploy:192.168.175.129]
url = http://192.168.175.129:6800/
username = root
password = toor
project = jd_book_detail

[deploy:192.168.175.132]
url = http://192.168.175.132:6800/
username = root
password = toor
project = jd_book_detail

[deploy:192.168.88.14]
url = http://192.168.88.14:6800/
project = jd_book_detail

```

3. 使用`scrapyd-client`部署项目

进入爬虫项目目录，执行：
```
scrapyd-deploy [target] -p jd_book_detail #target即scrapy.cfg文件中deploy后的名称，可以使用`-a`参数向所有服务器部署
```

4. 通过scrapyd服务的控制接口启动爬虫
```
curl http://x.x.x.x:6800/schedule.json -d project=myproject -d spider=somespider
```
**注意：**如果是windows，可以使用requests调用scrapyd接口实现爬虫项目调度，参考：[https://segmentfault.com/a/1190000020343777](https://segmentfault.com/a/1190000020343777)

## 使用gerapy图形界面化部署/调度爬虫项目（替代scrapyd-client）

- 简述
```
gerapy init #初始化
cd gerapy && gerapy migrate #初始化sqlite3数据库
gerapy runserver 0.0.0.0:8000

```
参考：[https://cuiqingcai.com/4959.html](https://cuiqingcai.com/4959.html)

- 可能遇到的问题

参考：

[https://www.cnblogs.com/lutt/p/12344990.html](https://www.cnblogs.com/lutt/p/12344990.html)

[https://www.cnblogs.com/vilogy/p/12405662.html](https://www.cnblogs.com/vilogy/p/12405662.html)

[https://blog.csdn.net/Tiger_lin1/article/details/106168011](https://blog.csdn.net/Tiger_lin1/article/details/106168011)

