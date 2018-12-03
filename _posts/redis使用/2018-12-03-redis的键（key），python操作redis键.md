---
layout: default 
author: muyalei
date: 2018-12-03
title: redis的键（key），python操作redis键
tags:
   - redis
---


***转载自[https://www.cnblogs.com/xuchunlin/p/7061524.html](https://www.cnblogs.com/xuchunlin/p/7061524.html)***


1. delete DEL 命令用于删除已存在的键。不存在的 key 会被忽略
```
print r.set('1', '4028b2883d3f5a8b013d57228d760a93') #set 设置指定 key 的值， 如果设置正确返回 True

print r.get('1') # 得到 键为1 的值    4028b2883d3f5a8b013d57228d760a93

print r.delete('1') # 删除 键为1 的值

print r.get('1')    #因为上面已经把键为1 的值删除掉，所以返回的是None
```
2. exists
```
#设定键为2的值是  4028b2883d3f5a8b013d57228d760a93
r.set('2', '4028b2883d3f5a8b013d57228d760a93')
# 存在就返回True 不存在就返回False
print r.exists('2')  #返回True
print r.exists('33')  #返回False
```
3. Expire 命令用于设置 key 的过期时间。key 过期后将不再可用。
```
r.set('2', '4028b2883d3f5a8b013d57228d760a93')
#成功就返回True 失败就返回False，下面的20表示是20秒
print r.expire('2',20)
#如果时间没事失效我们能得到键为2的值，否者是None
print r.get('2')
```
4.  Expireat 命令用于以 UNIX 时间戳(unix timestamp)格式设置 key 的过期时间。key 过期后将不再可用。主意:时间精确到秒，时间戳是10为数字
```
r.set('2', '4028b2883d3f5a8b013d57228d760a93')
#成功就返回True 失败就返回False，下面的1598033936表示是在2020-08-22 02:18:56 键2 过期
print r.expireat('2',1598033936)
print r.get('2')
```
5.PEXPIREAT 命令用于设置 key 的过期时间，已毫秒技。key 过期后将不再可用。主意:时间精确到毫秒，时间戳是13位数字
```
r.set('2', '4028b2883d3f5a8b013d57228d760a93')
#成功就返回True 失败就返回False。
print r.expireat('2',1598033936000)
print r.get('2')
```
6. Keys 命令用于查找所有符合给定模式 pattern 的 key 。
```
print r.set('111', '11')
print r.set('122', '12')
print r.set('113', '13')
print r.keys(pattern='11*')
# 输出的结果是 ['113', '111'] 因为键122不和 11* 匹配
```
7. MOVE 命令用于将当前数据库的 key 移动到给定的数据库 db 当中,select可以设定当前的数据库，如有需要请看select命令
```
因为我们默认使用的数据库是db0，我们可以使用下面的命令键 2 移动到数据库 1 中去
r.move(2,1)
```
8. PERSIST 命令用于移除给定 key 的过期时间，使得 key 永不过期
```
#设定键为 1 的值为11
print r.set('1', '11')
#设定键 1 过期时间为100秒
print r.expire(1,100)
# 查看键 1 的过期时间还剩下多少
print r.ttl('1')
# 目的是13秒后移除键 1 的过期时间
import time
time.sleep(3)
# 查看键 1 的过期时间还剩下多少
print r.ttl('1')
#移除键 1 的过期时间
r.persist(1)
# 查看键 1 的过期时间还剩下多少  输出的结果是 None，我们可以通过redis desktop manager 查看键 1 的过期时间
print r.ttl('1')
```
9. Pttl 命令以毫秒为单位返回 key 的剩余过期时间。
```
# 当 key 不存在时，返回 -2 。 当 key 存在但没有设置剩余生存时间时，返回 -1 。 否则，以毫秒为单位，返回 key 的剩余生存时间。
#设定键为 1 的值为11
print r.set('1', '11')
#设定键 1 过期时间为100秒
print r.expire(1,100)
import time
time.sleep(3)
#返回的结果是 96994 ，运行的结果不是固定的，大于是97秒钟，主意是为了展示出返回的结果是毫秒，一秒等于1000毫秒
print r.pttl('1')
```
10. TTL 命令以秒为单位返回 key 的剩余过期时间。
```
# 当 key 不存在时，返回 -2 。 当 key 存在但没有设置剩余生存时间时，返回 -1 。 否则，以毫秒为单位，返回 key 的剩余生存时间。
#设定键为 1 的值为11
print r.set('1', '11')
print r.expire(1,100)   #设定键 1 过期时间为100秒
import time
time.sleep(3)
print r.ttl('1') #返回的结果是 97
print r.ttl('123') #因为键 123 不存在  所以返回的结果是None
```
11. RANDOMKEY 命令从当前数据库中随机返回一个 key。当数据库不为空时，返回一个 key 。 当数据库为空时，返回 nil 。
```
print r.randomkey() #数据库返回的是默认的数据库 key
```
12. Rename 命令用于修改 key 的名称 。改名成功时提示 OK ，失败时候返回一个错误。
```
print r.rename(1,1111) #修改成功返回 True
print r.rename(222,1111) #如果key 不存在 修改失败返回 redis.exceptions.ResponseError: no such key
```
13. Renamenx 命令用于在新的 key 不存在时修改 key 的名称 。
```
print r.exists(123123) #返回false
print r.renamenx(1111,123123) #成功返回True
print r.renamenx(1111,123123) #失败返回    redis.exceptions.ResponseError: no such key
```
14. Type 命令用于返回 key 所储存的值的类型
```
# 返回 key 的数据类型，数据类型有：none (key不存在)，string (字符串)，list (列表)，set (集合)，zset (有序集)，hash (哈希表)，
print r.set('1',"111111111")
print r.type('1') #返回的结果是string

print r.sadd('2','222222222222')
print r.type('2') #返回的结果是set

print r.lpush('3','33333333')
print r.type('3') #返回的结果是list
```
 
******

命令：

- Redis DEL 命令	该命令用于在 key 存在是删除 key。
- Redis Dump 命令		序列化给定 key ，并返回被序列化的值。
- Redis EXISTS 命令	检查给定 key 是否存在。
- Redis Expire 命令	seconds 为给定 key 设置过期时间。
- Redis Expireat 命令		EXPIREAT 的作用和 EXPIRE 类似，都用于为 key 设置过期时间。不同在于 EXPIREAT 命令接受的时间参数是 UNIX 时间戳(unix timestamp)。
- Redis PEXPIREAT 命令	设置 key 的过期时间亿以毫秒计。
- Redis PEXPIREAT 命令	设置 key 过期时间的时间戳(unix timestamp) 以毫秒计
- Redis Keys 命令		查找所有符合给定模式( pattern)的 key 。
- Redis Move 命令		将当前数据库的 key 移动到给定的数据库 db 当中。
- Redis PERSIST 命令	移除 key 的过期时间，key 将持久保持。
- Redis Pttl 命令		以毫秒为单位返回 key 的剩余的过期时间。
- Redis TTL 命令	以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。
- Redis RANDOMKEY 命令	从当前数据库中随机返回一个 key 。
- Redis Rename 命令	修改 key 的名称
- Redis Renamenx 命令		仅当 newkey 不存在时，将 key 改名为 newkey 。
- Redis Type 命令	返回 key 所储存的值的类型。
