---
layout: default
author: muyalei
date: 2018-11-30
title: redis的hash详解
tags:
   - redis
---

***整理自[https://www.cnblogs.com/xuchunlin/p/7064860.html](https://www.cnblogs.com/xuchunlin/p/7064860.html)***

 
1. Hset 命令用于为哈希表中的字段赋值 。如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。如果字段已经存在于哈希表中，旧值将被覆盖。<br/>
如果字段是哈希表中的一个新建字段，并且值设置成功，返回 1 。 如果哈希表中域字段已经存在且旧值已被新值覆盖，返回 0 。
```
print r.hset(name="name",key="key1",value="value")  #返回的结果是 1
print r.hget(name="name",key="key1")    #返回的结果是 value
print r.hset(name="name",key="key1",value="hello world")  #返回的结果是 0,原因是哈希表中域字段已经存在且旧值已被新值覆盖
print r.hget(name="name",key="key1")    #返回的结果是 hello world
```
2. Hdel 命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.delete(1)    # 删除成功后 返回的结果是 1
print r.delete(1)    # 因为上一步已经删除，删除失败后 返回的结果是 0
```
3. Hexists  命令用于查看哈希表的指定字段是否存在。如果哈希表含有给定字段，返回 True 。 如果哈希表不含有给定字段，或 key 不存在，返回False 。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hexists(name="1",key="1")   # 返回的结果是 True
print r.hexists(name="1",key="2")   # 返回的结果是 False
print r.hexists(name="2",key="2")   # 返回的结果是 False
print r.hexists(name="2",key="1")   # 返回的结果是 False
```
4. Hget 命令用于返回哈希表中指定字段的值。返回给定字段的值。如果给定的字段或 key 不存在时，返回 None 。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hget("1","1")   # 返回的结果是 1
print r.hget("2","1")   # 因为字段2不存在。所以返回的结果是 None
print r.hget("1","2")   # 因为key 2 不存在。所以返回的结果是 None
print r.hget("2","2")   # 因为key和字段都不存在，所以返回的结果是 None
```
5. Hgetall 命令用于返回哈希表中，所有的字段和值。在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，所以返回值的长度是哈希表大小的两倍。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hset(name="1", key="3", value="2")  # 返回的结果是 1
print r.hset(name="1", key="2", value="3")  # 返回的结果是 1
print r.hset(name="1", key="2", value="4")  # 返回的结果是 0   如果不知道为什么返回的结果是0，请看hset
print r.hgetall("1")    # 返回的结果是 {'1': '1', '3': '2', '2': '4'}  主意返回的数据格式
print r.hgetall("2")    # 因为字典名2 不存在，所以返回的结果是 {}
``` 

在数据库中存储的数据格式
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的hash详解_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的hash详解_图片1.png)
![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的hash详解_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的hash详解_图片2.png)

6. Hincrby 命令用于为哈希表中的字段值加上指定增量值。<br/>
增量也可以为负数，相当于对指定字段进行减法操作。<br/>
如果哈希表的 key 不存在，一个新的哈希表被创建并执行 HINCRBY 命令。<br/>
如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。<br/>
对一个储存字符串值的字段执行 HINCRBY 命令将造成一个错误。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hincrby(name="1",key="1",amount=2)  # 返回的结果是 3
print r.hget(name="1",key="1")              # 返回的结果是 3
print r.hincrby(name="2", key="2", value="3")  # 字段不存在，返回的结果是 TypeError: hincrby() got an unexpected keyword argument 'value'
print r.hincrby(name="1",key="2",amount=4)  # 这步是因为key为2不存在，返回的结果是 4，说明哈希表的 key 不存在，一个新的哈希表被创建并执行 HINCRBY 命令
print r.hget(name="1",key="2")              # 返回的结果是 4
```
7. Hincrbyfloat 命令用于为哈希表中的字段值加上指定浮点数增量值。<br/>
如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。<br/>
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hincrbyfloat(name="1",key="1",amount="1.2")  # 返回的结果是 2.2
print r.hget("1","1")        # 返回的结果是 2.2
print r.hincrbyfloat(name="2",key="1",amount="1.2")  # 指定的字段2不存在，返回的结果是 1.2，说明如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0
``` 
8. Hkeys 命令用于获取哈希表中的所有字段名。包含哈希表中所有字段的列表。 当 key 不存在时，返回一个空列表。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hset(name="1", key="1", value="2")  # 返回的结果是 0
print r.hset(name="1", key="2", value="2")  # 返回的结果是 1
print r.hset(name="1", key="3", value="2")  # 返回的结果是 1
print r.hkeys(1)                            # 返回的结果是 ['1', '2', '3']
print r.hkeys(2)                            # 因为指定的字段名不存在，所以返回的结果是 []
```
9. Hlen 命令用于获取哈希表中字段的数量。哈希表中字段的数量。 当 key 不存在时，返回 0 。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hset(name="1", key="2", value="2")  # 返回的结果是 1
print r.hlen(1)                             # 返回的结果是 2
print r.hset(name="1", key="4", value="3")  # 返回的结果是 1
print r.hset(name="1", key="3", value="2")  # 返回的结果是 1
print r.hlen(1)                             # 返回的结果是 4
```
10. Hmget 命令用于返回哈希表中，一个或多个给定字段的值。如果指定的字段不存在于哈希表，那么返回一个 nil 值。<br/>
一个包含多个给定字段关联值的表，表值的排列顺序和指定字段的请求顺序一样。
```
print r.hset(name="1", key="1", value="1")  # 返回的结果是 1
print r.hset(name="1", key="2", value="2")  # 返回的结果是 1
print r.hmget(name="1",keys="1")             # 返回的结果是 ['1']
print r.hmget(name="1",keys="2")             # 返回的结果是['2']
print r.hmget(name="2",keys="1")             # 返回的结果是 [None]
```
11. Hmset 命令用于同时将多个 field-value (字段-值)对设置到哈希表中。<br/>
此命令会覆盖哈希表中已存在的字段。<br/>
如果哈希表不存在，会创建一个空哈希表，并执行 HMSET 操作。
```
aa = {"a":"a","b":"b"}           # 返回的结果是 ['1']
print r.hmset("name",aa)            # 返回的结果是 True
print r.hget(name="name",key="a")   # 返回的结果是 a
print r.hget(name="name",key="b")   # 返回的结果是 b
```
12. Hsetnx 命令用于为哈希表中不存在的的字段赋值 。<br/>
如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。<br/>
如果字段已经存在于哈希表中，操作无效。<br/>
如果 key 不存在，一个新哈希表被创建并执行 HSETNX 命令。<br/>
设置成功，返回 1 。 如果给定字段已经存在且没有操作被执行，返回 0 
```。
print r.hsetnx(name="1",key="1",value="1")   # 返回的结果是 1
print r.hsetnx(name="1",key="1",value="2")   # 返回的结果是 0
print r.hsetnx(name="2",key="1",value="2")   # 返回的结果是 0
```
13. Hvals 命令返回哈希表所有字段的值。一个包含哈希表中所有值的表。 当 key 不存在时，返回一个空表。
```
print r.hset(name="1", key="1", value="11")  # 返回的结果是 1
print r.hset(name="1", key="2", value="22")  # 返回的结果是 1
print r.hset(name="1", key="3", value="33")  # 返回的结果是 1
print r.hset(name="1", key="4", value="44")  # 返回的结果是 1
print r.hvals("1")                          # 返回的结果是 ['11', '22', '33', '44']
print r.hvals("2")                          # 返回的结果是 []
```

********

#### redis hash 命令

- Redis Hdel 命令	删除一个或多个哈希表字段
- Redis Hexists 命令	查看哈希表 key 中，指定的字段是否存在。
- Redis Hget 命令	获取存储在哈希表中指定字段的值/td>
- Redis Hgetall 命令	获取在哈希表中指定 key 的所有字段和值
- Redis Hincrby 命令	为哈希表 key 中的指定字段的整数值加上增量 increment 。
- Redis Hincrbyfloat 命令	为哈希表 key 中的指定字段的浮点数值加上增量 increment 。
- Redis Hkeys 命令	获取所有哈希表中的字段
- Redis Hlen 命令	获取哈希表中字段的数量
- Redis Hmget 命令	获取所有给定字段的值
- Redis Hmset 命令	同时将多个 field-value (域-值)对设置到哈希表 key 中。
- Redis Hset 命令	将哈希表 key 中的字段 field 的值设为 value 。
- Redis Hsetnx 命令	只有在字段 field 不存在时，设置哈希表字段的值。
- Redis Hvals 命令	获取哈希表中所有值

