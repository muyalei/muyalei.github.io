---
layout: default
author: muyalei
date: 2018-11-30
title: redis的sorted set详解
tags:
   - redis
---

***整理自[https://www.cnblogs.com/xuchunlin/p/7097255.html](https://www.cnblogs.com/xuchunlin/p/7097255.html)***


1. Zadd 命令用于将一个或多个成员元素及其分数值加入到有序集当中。<br/>
如果某个成员已经是有序集的成员，那么更新这个成员的分数值，并通过重新插入这个成员元素，来保证该成员在正确的位置上。<br/>
分数值可以是整数值或双精度浮点数。<br/>
如果有序集合 key 不存在，则创建一个空的有序集并执行 ZADD 操作。<br/>
当 key 存在但不是有序集类型时，返回一个错误。
```
print r.zadd("1","1",2,"3",3) #输出的结果是2
print r.zadd("1","2",2)     #输出的结果是1
print r.zadd("1","1",1)     #输出的结果是0
print r.zadd("1","3",4)     #输出的结果是0
print r.zrange("1",0,-1)    #输出的结果是 ['1', '2', '3']
```
2. Zcard 命令用于计算集合中元素的数量。<br/>
当 key 存在且是有序集类型时，返回有序集的基数。 当 key 不存在时，返回 0 。
```
print r.zadd("1","1",1,"3",3) #输出的结果是2
print r.zadd("1","2",2)     #输出的结果是1
print r.zadd("1","2",4)     #输出的结果是1
print r.zcard(1)            #输出的结果是3
print r.zcard(2)            #输出的结果是0
```
3. Zcount 命令用于计算有序集合中指定分数区间的成员数量。分数值在 min 和 max 之间的成员的数量。
```
print r.zadd("2","1",1,"3",3) #输出的结果是2
print r.zadd("2","2",2)     #输出的结果是1
print r.zadd("2","1",4)     #输出的结果是0
print r.zcount("2",min=0,max=5)     #输出的结果是3
print r.zcount("2",min=0,max=3)     #输出的结果是2
print r.zcount("2",min=1,max=3)     #输出的结果是2
```
4. Zincrby 命令对有序集合中指定成员的分数加上增量 increment<br/>
可以通过传递一个负数值 increment ，让分数减去相应的值，比如 ZINCRBY key -5 member ，就是让 member 的 score 值减去 5 。<br/>
当 key 不存在，或分数不是 key 的成员时， ZINCRBY key increment member 等同于 ZADD key increment member 。<br/>
当 key 不是有序集类型时，返回一个错误。<br/>
分数值可以是整数值或双精度浮点数。<br/>
member 成员的新分数值，以字符串形式表示。
```
print r.zadd("4","1",1,"2",2,"3",3,"4",4)   #输出的结果是4
print r.zincrby(name=4,value=1,amount=5)    #输出的结果是6.0
print r.zincrby(name=4,value=2,amount=55)    #输出的结果是57.0
print r.zrange(name=4,start=0,end=-1,withscores=False)       #输出的结果是['1', '3', '2', '4']
```
5. Zinterstore 命令计算给定的一个或多个有序集的交集，其中给定 key 的数量必须以 numkeys 参数指定，并将该交集(结果集)储存到 destination 。<br/>
默认情况下，结果集中某个成员的分数值是所有给定集下该成员分数值之和。
```
print r.zadd("41", "a1", 6, "a2", 2,"a3",5)     #输出的结果是3
print r.zadd('42', a1=7,b1=10, b2=5)            #输出的结果是3
# 获取两个有序集合的交集并放入dest集合，如果遇到相同值不同分数，则按照aggregate进行操作
# aggregate的值为: SUM  MIN  MAX
print r.zinterstore("43",("42","41"),aggregate="MAX")       #输出的结果是4
print(r.zscan("43"))                                        #输出的结果是(0L, [('a1', 7.0)])
```
6. Zlexcount 命令在计算有序集合中指定字典区间内成员数量。
```
print r.zadd("6", "a", 1, "b", 2,"c",3)     #输出的结果是3
print r.zlexcount(name=6,min="-",max="+")   #输出的结果是3
print r.zadd("6", "e", 4, "f", 5,"d",6)     #输出的结果是3
print r.zlexcount(name=6,min="-",max="+")   #输出的结果是6
print r.zlexcount(name=6,min="[a",max="[b")   #输出的结果是2
print r.zlexcount(name=6,min="[a",max="[f")   #输出的结果是6
print r.zlexcount(name=6,min="[a",max="[e")   #输出的结果是4
```
7. Zrange 返回有序集中，指定区间内的成员。<br/>
其中成员的位置按分数值递增(从小到大)来排序。<br/>
具有相同分数值的成员按字典序(lexicographical order )来排列。<br/>
如果你需要成员按值递减(从大到小)来排列，请使用 ZREVRANGE 命令。<br/>
下标参数 start 和 stop 都以 0 为底，也就是说，以 0 表示有序集第一个成员，以 1 表示有序集第二个成员，以此类推。<br/>
你也可以使用负数下标，以 -1 表示最后一个成员， -2 表示倒数第二个成员，以此类推。<br/>
```
print r.zadd("7", "1", 1, "2", 2,"3",3,"4",4,"5",5)     #输出的结果是5
print r.zrange("7",start=0,end=-1,desc=False)           #输出的结果是['1', '2', '3', '4', '5']
print r.zrange("7",start=0,end=2,desc=False)            #输出的结果是['1', '2', '3']
```
8. Zrangebylex 通过字典区间返回有序集合的成员。<br/>
当有序集合的所有成员都具有相同的分值时，有序集合的元素会根据成员的 值 （lexicographical ordering）来进行排序，而这个命令则可以返回给定的有序集合键 key 中， 元素的值介于 min 和 max 之间的成员<br/>
对集合中的每个成员进行逐个字节的对比（byte-by-byte compare）， 并按照从低到高的顺序， 返回排序后的集合成员。 如果两个字符串有一部分内容是相同的话， 那么命令会认为较长的字符串比较短的字符串要大
```
print r.zadd("8", "a", 1, "b", 2,"c",3)     #输出的结果是3
print r.zrangebylex(name="8",min="-",max="[c")   #输出的结果是 ['a', 'b', 'c']
print r.zrangebylex(name="8",min="-",max="(c")   #输出的结果是 ['a', 'b']
print r.zadd("8", "e", 4, "f", 5,"d",6)     #输出的结果是3
print r.zrangebylex(name=8,min="[b",max="[f")   #输出的结果是 ['b', 'c', 'e', 'f', 'd']
print r.zrangebylex(name=8,min="(b",max="[f")   #输出的结果是 ['c', 'e', 'f', 'd']
```
9. Zrangebyscore 返回有序集合中指定分数区间的成员列表。有序集成员按分数值递增(从小到大)次序排列。<br/>
具有相同分数值的成员按字典序来排列(该属性是有序集提供的，不需要额外的计算)。<br/>
默认情况下，区间的取值使用闭区间 (小于等于或大于等于)，你也可以通过给参数前增加 ( 符号来使用可选的开区间 (小于或大于)。
```
print r.zadd("9", "a", 1, "b", 2,"c",3)     #输出的结果是3
print r.zrangebyscore("9","1","6")  #输出的结果是['a', 'b', 'c']
print r.zadd("9", "c", 11, "d", 21,"e",32)     #输出的结果是3
print r.zrangebyscore("9","3","16")  #输出的结果是['c']
print r.zrangebyscore("9","3","36")  #输出的结果是['c', 'd', 'e']
```
10. Zrank 返回有序集中指定成员的排名。其中有序集成员按分数值递增(从小到大)顺序排列。<br/>
如果成员是有序集 key 的成员，返回 member 的排名。 如果成员不是有序集 key 的成员，返回 None 。
```
print r.zadd("10", "a", 1, "b", 2, "c", 3)  # 输出的结果是3
print r.zadd("10", "f", 11, "d", 21,"e",32)    #输出的结果是3
print r.zrank("10","a")                     #输出的结果是0
print r.zrank("10","b")                     #输出的结果是1
print r.zrank("10","e")                     #输出的结果是5
print r.zrank("10","d")                     #输出的结果是4
print r.zrank("10","h")                     #输出的结果是None
```
11. Zrem 命令用于移除有序集中的一个或多个成员，不存在的成员将被忽略。<br/>
当 key 存在但不是有序集类型时，返回一个错误。
```
print r.zadd("11", "a", 1, "b", 2, "c", 3)  # 输出的结果是3
print r.zadd("11", "f", 11, "d", 21,"e",32) #输出的结果是3
print r.zrem("11","a")                      #输出的结果是1
print r.zrem("11","f")                      #输出的结果是1
print r.zrem("11","h")                      #输出的结果是0
print r.zrange("11",start=0,end=32)         #输出的结果是['b', 'c', 'd', 'e'], 其中  a f 已经移除掉
print r.zrange("11",start=2,end=32)         #输出的结果是['d', 'e'], 其中  a f 已经移除掉，d  e  没有被包涵
```
12. Zremrangebylex 命令用于移除有序集合中给定的字典区间的所有成员。<br/>
被成功移除的成员的数量，不包括被忽略的成员。
```
print r.zadd("12", "a", 1, "b", 2, "c", 3)         # 输出的结果是3
print r.zadd("12", "d", 11, "e", 21,"f",32)        #输出的结果是3
print r.zremrangebylex("12",min="[a",max="[c")    #输出的结果是3
print r.zrange("12",0,-1)                         #输出的结果是 ['d', 'e', 'f']  因为  a，b，c已经被移除
```
13. Zremrangebyrank 命令用于移除有序集中，指定排名(rank)区间内的所有成员。
```
# print r.zadd("13", "a", 1, "b", 2, "c", 3)         # 输出的结果是3
# print r.zadd("13", "d", 8, "e", 21,"f",32)        #输出的结果是3
# print r.zremrangebyrank(name=13,min=1,max=3)       #输出的结果是3
# print r.zrange("13","0","-1")                      #输出的结果是['a', 'e', 'f']  因为删除了 b，c，d
```
14. Zremrangebyscore 命令用于移除有序集中，指定分数（score）区间内的所有成员。
```
print r.zadd("14", "a", 1, "b", 2, "c", 3)          #输出的结果是3
print r.zadd("14", "d", 8, "e", 21,"f",32)          #输出的结果是3
print r.zremrangebyscore(name="14",min="1",max="8")       #输出的结果是4,删除的a，b，c，d
print r.zrange(name="14",start=0,end=-1)            #输出的结果是 ['e', 'f']
```
15.Zrevrange 命令返回有序集中，指定区间内的成员。<br/>
其中成员的位置按分数值递减(从大到小)来排列。<br/>
具有相同分数值的成员按字典序的逆序(reverse lexicographical order)排列。<br/>
除了成员按分数值递减的次序排列这一点外， ZREVRANGE 命令的其他方面和 ZRANGE 命令一样。
```
print r.zadd("15", "a", 1, "b", 2, "c", 3)          #输出的结果是3
print r.zadd("15", "d", 8, "e", 21,"f",32)          #输出的结果是3
print r.zrevrange(name="15",start=0,end=-1)         #输出的结果是['f', 'e', 'd', 'c', 'b', 'a']
print r.zrevrange(name="15",start=1,end=21)         #输出的结果是['e', 'd', 'c', 'b', 'a']
print r.zrevrange(name="15",start=3,end=21)         #输出的结果是['c', 'b', 'a']
```
16. Zrevrangebyscore 返回有序集中指定分数区间内的所有的成员。有序集成员按分数值递减(从大到小)的次序排列。<br/>
具有相同分数值的成员按字典序的逆序(reverse lexicographical order )排列。<br/>
除了成员按分数值递减的次序排列这一点外， ZREVRANGEBYSCORE 命令的其他方面和 ZRANGEBYSCORE 命令一样。
```
print r.zadd("16", "a", 1, "b", 2, "c", 3)          #输出的结果是3
print r.zadd("16", "d", 8, "e", 21,"f",32)          #输出的结果是3
print r.zrevrangebyscore(name="16",max=33,min=0)    #输出的结果是['f', 'e', 'd', 'c', 'b', 'a']
print r.zrevrangebyscore(name="16",max=20,min=2)    #输出的结果是['d', 'c', 'b']
```
17. Zrevrank 命令返回有序集中成员的排名。其中有序集成员按分数值递减(从大到小)排序。<br/>
排名以 0 为底，也就是说， 分数值最大的成员排名为 0 。<br/>
使用 ZRANK 命令可以获得成员按分数值递增(从小到大)排列的排名。
```
print r.zadd("17", "a", 1, "b", 2, "c", 3)          #输出的结果是3
print r.zadd("17", "d", 4, "e", 5,"f",6)            #输出的结果是3
print r.zrevrank(name=17,value="a")                 #输出的结果是5
print r.zrevrank(name=17,value="c")                 #输出的结果是3
print r.zrevrank(name=17,value="d")                 #输出的结果是2
print r.zrevrank(name=17,value="h")                 #输出的结果是None
```
18. Zscore 命令返回有序集中，成员的分数值。 如果成员元素不是有序集 key 的成员，或 key 不存在，返回 None 。
```
print r.zadd("18", "a", 1, "b", 2, "c", 3)   #输出的结果是3
print r.zadd("18", "d", 4, "e", 5,"f",6)     #输出的结果是3
print r.zscore(name="18",value="a")          #输出的结果是1.0
print r.zscore(name="18",value="c")          #输出的结果是3.0
print r.zscore(name="18",value="f")          #输出的结果是6.0
print r.zscore(name="18",value="h")          #输出的结果是None
```
19. Zunionstore 命令计算给定的一个或多个有序集的并集，其中给定 key 的数量必须以 numkeys 参数指定，并将该并集(结果集)储存到 destination 。<br/>
默认情况下，结果集中某个成员的分数值是所有给定集下该成员分数值之和 。<br/>
保存到 destination 的结果集的成员数量。
 
20.  Zscan 命令用于迭代有序集合中的元素（包括元素成员和元素分值）<br/>
返回的每个元素都是一个有序集合元素，一个有序集合元素由一个成员（member）和一个分值（score）组成。
```
print r.zadd("20", "a", 1, "b", 2, "c", 3)   #输出的结果是3
print r.zscan(name="20")                     #输出的结果是(0L, [('a', 1.0), ('b', 2.0), ('c', 3.0)])
print r.zadd("20", "d", 4, "e", 5,"f",3)     #输出的结果是3
print r.zscan(name="20")                     #输出的结果是 (0L, [('a', 1.0), ('b', 2.0), ('c', 3.0), ('f', 3.0), ('d', 4.0), ('e', 5.0)])
```
