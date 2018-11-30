---
layout: default
author: muyalei
date: 2018-11-30
title: redis的list详解
tags:
   - redis
---

***整理自[https://www.cnblogs.com/xuchunlin/p/7067154.html](https://www.cnblogs.com/xuchunlin/p/7067154.html)***


1. Lpush 命令将一个或多个值插入到列表头部。 如果 key 不存在，一个空列表会被创建并执行 LPUSH 操作。 当 key 存在但不是列表类型时，返回一个错误。<br/>
   执行 LPUSH 命令后，列表的长度:
   ```
   print r.lpush("1",1)  #输出的结果是1
   print r.lpush("1",1)  #输出的结果是2
   print r.lpush("1",2,3,4)  #输出的结果是5
   print r.set("2",1)   #输出的结果是 True
   print r.lpush("2",2)     #输出的结果是 redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value,原因是键 2 是字符串类型，我们用list中的lpush给他添加元素
   ```
2. Rpush 命令用于将一个或多个值插入到列表的尾部(最右边)。<br/>
   如果列表不存在，一个空列表会被创建并执行 RPUSH 操作。 当列表存在但不是列表类型时，返回一个错误。<br>
   执行 RPUSH 操作后，列表的长度:
   ```
   print r.rpush("2",1)     #输出的结果是1
   print r.rpush("2",2,3)   #输出的结果是3
   print r.rpush("2",4,5)   #输出的结果是5
   ```
   数据格式：　　　　　　　　　　
   ![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片1.png)

3. Blpop 命令移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。<br/>
   如果列表为空，返回一个 None 。 否则，返回一个含有两个元素的列表，第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。
   ```
   print r.rpush("3",1,2,3,4,5,6,)      #输出的结果是6
   print r.blpop("3")                   #输出的结果是('3', '1')
   print r.blpop("3")                   #输出的结果是('3', '2')
   print r.blpop("3")                   #输出的结果是('3', '3')
   print r.blpop("4",timeout=2)         #因为键 4 不存在，所以2秒后输出的结果是None
   ```
4. Brpop 命令移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。<br/>
   假如在指定时间内没有任何元素被弹出，则返回一个None 和等待时长。 反之，返回一个含有两个元素的列表，第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。
   ```
   print r.rpush("4",1,2,3,4,5,6,)      #输出的结果是6
   print r.brpop("4")      #输出的结果是('4', '6')
   print r.brpop("4")      #输出的结果是('4', '5')
   print r.brpop("4")      #输出的结果是('4', '4')
   print r.brpop("5",timeout=2)      #因为键 4 不存在，所以2秒后输出的结果是None
   ```
5. Brpoplpush 命令从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。<br>
   假如在指定时间内没有任何元素被弹出，则返回一个 None 和等待时长。 反之，返回一个含有两个元素的列表，第一个元素是被弹出元素的值，第二个元素是等待时长。
   ```
   print r.rpush("11",1,2,3)      #输出的结果是3
   print r.rpush("22",4,5,6,)      #输出的结果是3
   print r.brpoplpush(src="11",dst="22",timeout=2)  #输出的结果是3
   print r.brpoplpush(src="44",dst="22",timeout=2)  #键44 不存在，输出的结果是None
   ```
   键 11 的值：<br/>  
   ![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片2.png)

   键22 的值：<br/>
   ![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片3.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片3.png)

6. Lindex 命令用于通过索引获取列表中的元素。你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。<br/>
   列表中下标为指定索引值的元素。 如果指定索引值不在列表的区间范围内，返回 None 。
   ```
   print r.rpush("6",1,2,3)      #输出的结果是3
   print r.lindex("6",1)        #输出的结果是2
   print r.lindex("6",2)        #输出的结果是3
   print r.lindex("6",3)        #输出的结果是None
   print r.lindex("6",4)        #输出的结果是None
   print r.lindex("6",-1)       #输出的结果是3
   ```
7. Linsert 命令用于在列表的元素前或者后插入元素。<br/>
   当指定元素不存在于列表中时，不执行任何操作。 当列表不存在时，被视为空列表，不执行任何操作。 如果 key 不是列表类型，返回一个错误。<br/>
   如果命令执行成功，返回插入操作完成之后，列表的长度。 如果没有找到指定元素 ，返回 -1 。 如果 key 不存在或为空列表，返回 0 。
   ```
   print r.rpush("7",1)      #输出的结果是1
   print r.rpush("7",2)      #输出的结果是2
   print r.linsert("7","BEFORE","2",12)    #输出的结果是2
   ```
   插入后的结果是：
   ![https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片4.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2018-11-30-redis的list详解_图片4.png)

8. Llen 命令用于返回列表的长度。 如果列表 key 不存在，则 key 被解释为一个空列表，返回 0 。 如果 key 不是列表类型，返回一个错误。
   ```
   print r.llen("8")       #key 不存在，输出的结果是0
   print r.rpush("8",1)    #输出的结果是1
   print r.llen("8")       #输出的结果是1
   print r.rpush("8",2,3)    #输出的结果是3
   print r.llen("8")       #输出的结果是3
   ```
9. Lpop 命令用于移除并返回列表的第一个元素。<br/>
   列表的第一个元素。 当列表 key 不存在时，返回 None 。
   ```
   print r.lpop("9")       #输出的结果是None
   print r.rpush("9",1)    #输出的结果是1
   print r.rpush("9",2)    #输出的结果是2
   print r.lpop("9")       #输出的结果是1
   ```
   说明：被移除掉的是第一个值 1,  值2没有被移除

10. Lpushx 将一个或多个值插入到已存在的列表头部，列表不存在时操作无效。
   ```
   print r.rpush("10",1)       #输出的结果是1
   print r.rpushx("10",2)      #输出的结果是2
   print r.rpushx("10",3)      #输出的结果是3
   print r.rpushx("11",3)      #输出的结果是5
   print r.lrange("10",0,-1)   #输出的结果是['1', '2', '3']
   print r.lrange("11",0,-1)   #输出的结果是['1', '2', '1', '2', '3']
   ```
11. Lrange 返回列表中指定区间内的元素，区间以偏移量 START 和 END 指定。 其中 0 表示列表的第一个元素， 1 表示列表的第二个元素，以此类推。<br/>
   你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
   ```
   print r.rpush("11",1,2)       #输出的结果是2
   print r.rpush("11",3,4)       #输出的结果是4
   print r.lrange("11",0,-1)     #输出的结果是['1', '2', '3', '4']
   print r.lrange("11",1,2)      #输出的结果是['2', '3']
   ```
12. Lrem 根据参数 COUNT 的值，移除列表中与参数 VALUE 相等的元素。<br/>
   COUNT 的值可以是以下几种：<br/>
   count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。<br/>
   count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。<br/>
   count = 0 : 移除表中所有与 VALUE 相等的值。<br/>
   被移除元素的数量。 列表不存在时返回 0 。<br/>
   ```
   print r.rpush("12", 1)  # 输出的结果是1
   print r.rpush("12", 1)  # 输出的结果是2
   print r.rpush("12", 2)  # 输出的结果是3
   print r.rpush("12", 1)  # 输出的结果是4
   print r.lrem("12",1,-2) # 输出的结果是2
   print r.lrange("12",0,-1) # 输出的结果是['1', '2']
   ```
13. Lset 通过索引来设置元素的值。<br/>
   当索引参数超出范围，或对一个空列表进行 LSET 时，返回一个错误<br/>
   操作成功返回 True ，否则返回错误信息。
   ```
   print r.rpush("13",1,2,3,4)     # 输出的结果是4
   print r.lset("13",1,5)          # 输出的结果是True
   print r.lrange("13",0,-1)       # 输出的结果是['1', '5', '3', '4']
   ```
14. Ltrim 对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。<br/>
   下标 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。 <br/>
   你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
   ```
   print r.rpush("14",1,2,3,4)      # 输出的结果是4
   print r.ltrim("14",1,-2)         # 输出的结果是True
   print r.lrange("14",0,-1)        # 输出的结果是['2', '3']
   ```
15. Rpop 命令用于移除并返回列表的最后一个元素。<br/>
   列表的最后一个元素。 当列表不存在时，返回 None 。
   ```
   print r.rpush("15",1,2,3,4)     # 输出的结果是4
   print r.rpop("15")              # 输出的结果是4
   print r.lrange("15",0,-1)       # 输出的结果是['1', '2', '3']
   ```
16. Rpoplpush 命令用于移除列表的最后一个元素，并将该元素添加到另一个列表并返回。
   ```
   print r.rpush("16",1,2,3,4)     # 输出的结果是4
   print r.rpush("17",1,2,3,4)     # 输出的结果是4
   print r.rpoplpush("16","17")    # 输出的结果是4
   print r.lrange("16",0,-1)       # 输出的结果是['1', '2', '3']
   print r.lrange("17",0,-1)       # 输出的结果是['4', '1', '2', '3', '4']
   ```
17. Rpushx 命令用于将一个或多个值插入到已存在的列表尾部(最右边)。如果列表不存在，操作无效。
   ```
   print r.rpushx("18",1)       # 因为键18 不存在，所以插入失败，输出的结果是0
   print r.rpush("18",2)        # 输出的结果是1
   print r.rpushx("18",3)       # 输出的结果是2
   print r.lrange("18",0,-1)    # 输出的结果是['2', '3']
   ```

********

#### redis list命令

- Redis Blpop 命令	移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
- Redis Brpop 命令	移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
- Redis Brpoplpush 命令	从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
- Redis Lindex 命令	通过索引获取列表中的元素
- Redis Linsert 命令	在列表的元素前或者后插入元素
- Redis Llen 命令	获取列表长度
- Redis Lpop 命令	移出并获取列表的第一个元素
- Redis Lpush 命令	将一个或多个值插入到列表头部
- Redis Lpushx 命令	将一个或多个值插入到已存在的列表头部
- Redis Lrange 命令	获取列表指定范围内的元素
- Redis Lrem 命令	移除列表元素
- Redis Lset 命令	通过索引设置列表元素的值
- Redis Ltrim 命令	对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
- Redis Rpop 命令	移除并获取列表最后一个元素
- Redis Rpoplpush 命令	移除列表的最后一个元素，并将该元素添加到另一个列表并返回
- Redis Rpush 命令	在列表中添加一个或多个值
- Redis Rpushx 命令	为已存在的列表添加值
