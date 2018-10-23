---
layout:     post
title:      scrapy爬取到数据保存到mysql
subtitle:   scrapy
date:       2018-02-28
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - scrapy
---

### 示例源码
```
from twisted.enterprise import adbapi  #使用Twisted异步操作mysql
import MySQLdb
import MySQLdb.cursors


#Twisted只是提供一个异步容器，本身没提供数据库连接
class MysqlPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    #读取settings中配置的数据库参数
    @classmethod
    def from_settings(cls,settings):  #from_settings的用法，参考[scrapy官方文档](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/item-pipeline.html)中对from_crawler的描述
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8', #编码加上，否则可能出现中文乱码问题
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = False
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparams)  #**表示将字典扩展为关键字参数
        return cls(dbpool)  #相当于dbpool赋给了这个类，self中可以得到

    #pipeline默认调用的方法
    def process_item(self,item,spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是自己定义的函数
        query = self.dbpool.runInteraction(self._insert_into_table,item)
        query.addErrback(self._handle_error,item,spider)  #错误处理
        return item
    
    #执行具体的插入
    def _insert_into_table(self,tx,item):
        sqli = 'insert into ylmr_scrapy (城市,名称,联系电话,地址,来源,日期) values (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE 城市=%s,名称=%s,联系电话=%s,地址=%s,来源=%s,日期=%s'
        result = [item['city'],item['name'],item['tel'],item['address'],item['source'],item['date']]  #item是1个dict，将其转变成list
        tx.execute(sqli,result+result)

    #错误处理函数
    def _handle_error(self,failue,item,spider):
        print(failue)
```

最后，在settings配置，启用定义的pipeline类
'''
ITEM_PIPLINES = {
    'YlmrBaiduMap.piplines.MysqlPipeline':1  #数字越小，越优先执行
}
'''

### 注意事项
1.python版本高于3.4，导入MySQLdb，需要安装[Mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/)（注：Mysqlclient是MySQLdb连接库的一个分支，它修复了一些在MySQLdb连接路中存在的bug，并添加了对Python3的支持。Mysqlclient的底层是由C编写实现的，相比于PyMySQL，运行速度快一些。）；<br>
  Mysqlclient是MySQL-python的一个分支，但MySQL-python只支持到python3.4（包括3.4）。<br>
  也可以使用pymysql:<br>
  安装pymysql```pip install pymysql```，pipeline中```import pymysql、import pymysql.cursors```，将上述代码中'MySQLdb'出现的地方替换成'pymysql'即可<br>
  建议使用Mysqlclient，因为是用C编写，效率更高！<br>
 2.必须异步操作mysql，否则，可能出现丢失数据的情况（应该写入mysql的数据行没有写入）。
          
