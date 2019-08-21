---
layout: default
author: muyalei
tilte: mysql中primary key主键与unique键的区别以及作用
date: 2019-08-26
tags:
    - mysql相关
---


***整理自[https://www.cnblogs.com/demolzhi/p/6082298.html?utm_source=itdadao&utm_medium=referral](https://www.cnblogs.com/demolzhi/p/6082298.html?utm_source=itdadao&utm_medium=referral)***


```
共同作用是为了约束字段/建立索引/提高查询效率

　　　　　　mysql主键的属性：

　　　　　　　　　1.主键具有唯一性：是指一张表里只能有一个主键；

　　　　　　　　　2.主键作用：主键primary key是为了唯一标识一个字段，使其唯一且不能为NULL，自动生成索引；

　　　　　　　　　3.隐含定义：如果这些列没有被明确地定义为NOT NULL，MySQL会隐含地定义这些列。

 　　　　　　　　　　　4.主键其实也是索引，甚至在MySQL的术语里面“键”就等于“索引”，

　　　　　　　UNIQUE键的属性：

　　　　　　　　　1.唯一性：定义了UNIQUE约束的字段中不能包含重复值，

　　　　　　　　　2.可为空：在UNIQUE约束的字段上可以包含空值. 

 　　　　　　　　  3.扩展：unique就是唯一,当你需要限定你的某个表字段每个值都唯一,没有重复值时使用.

　　　　　　　　　 比如说,如果你有一个person_Info表,并且表中有个身份证的column,那么你就可以指定该字段unique. 

　　　　

关系：主键=NOT NULL +UNIQUE键的结合；

　　　　NOT NULL和UNIQUE约束最好的结合。如果这些列没有被明确地定义为NOT NULL，MySQL会隐含地定义这些列。

 

区别：　

　　(1) 唯一性约束所在的列允许空值，但是主键约束所在的列不允许空值。
　　(2) 可以把唯一性约束放在一个或者多个列上，这些列或列的组合必须有唯一的。但是，唯一性约束所在的列并不是表的主键列。
　　(3) 唯一性约束强制在指定的列上创建一个唯一性索引。在默认情况下，创建唯一性的非聚簇索引，但是，也可以指定所创建的索引是聚簇索引。

　　(4)建立主键的目的是让外键来引用.

　　(5)一个表最多只有一个主键，但可以有很多唯一键
```
