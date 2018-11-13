---
layout: default
author: muyalei
date: 2018-05-27
title: Django ORM之QuerySet
tags:
   - Django
---


***转载自[https://www.cnblogs.com/ajianbeyourself/p/3604332.html](https://www.cnblogs.com/ajianbeyourself/p/3604332.html)***

```
Django ORM用到三个类：Manager、QuerySet、Model。Manager定义表级方法（表级方法就是影响一条或多条记录的方法），我们可以以models.Manager为父类，定义自己的manager，增加表级方法；QuerySet：Manager类的一些方法会返回QuerySet实例，QuerySet是一个可遍历结构，包含一个或多个元素，每个元素都是一个Model 实例，它里面的方法也是表级方法，前面说了，Django给我们提供了增加表级方法的途径，那就是自定义manager类，而不是自定义QuerySet类，一般的我们没有自定义QuerySet类的必要；django.db.models模块中的Model类，我们定义表的model时，就是继承它，它的功能很强大，通过自定义model的instance可以获取外键实体等，它的方法都是记录级方法（都是实例方法，貌似无类方法），不要在里面定义类方法，比如计算记录的总数，查看所有记录，这些应该放在自定义的manager类中。以Django1.6为基础。

1.QuerySet
回到顶部
1.1 简介
每个Model都有一个默认的manager实例，名为objects，QuerySet有两种来源：通过manager的方法得到、通过QuerySet的方法得到。mananger的方法和QuerySet的方法大部分同名，同意思，如filter(),update()等，但也有些不同，如manager有create()、get_or_create()，而QuerySet有delete()等，看源码就可以很容易的清楚Manager类与Queryset类的关系，Manager类的绝大部分方法是基于Queryset的。一个QuerySet包含一个或多个model instance。QuerySet类似于Python中的list，list的一些方法QuerySet也有，比如切片，遍历。

>>> from userex.models import UserEx

>>> type(UserEx.objects)

<class ‘django.db.models.manager.Manager’>

>>> a = UserEx.objects.all()

>>> type(a)

<class ‘django.db.models.query.QuerySet’>

QuerySet是延迟获取的，只有当用到这个QuerySet时，才会查询数据库求值。另外，查询到的QuerySet又是缓存的，当再次使用同一个QuerySet时，并不会再查询数据库，而是直接从缓存获取（不过，有一些特殊情况）。一般而言，当对一个没有求值的QuerySet进行的运算，返回的是QuerySet、ValuesQuerySet、ValuesListQuerySet、Model实例时，一般不会立即查询数据库；反之，当返回的不是这些类型时，会查询数据库。下面介绍几种（并非全部）对QuerySet求值的场景。

class Blog(models.Model):

    name = models.CharField(max_length=100)

    tagline = models.TextField()

 

    def __unicode__(self):

        return self.name

 

class Author(models.Model):

    name = models.CharField(max_length=50)

    email = models.EmailField()

 

    def __unicode__(self):

        return self.name

 

class Entry(models.Model):

    blog = models.ForeignKey(Blog)

    headline = models.CharField(max_length=255)

    body_text = models.TextField()

    pub_date = models.DateField()

    mod_date = models.DateField()

    authors = models.ManyToManyField(Author)

    n_comments = models.IntegerField()

    n_pingbacks = models.IntegerField()

    rating = models.IntegerField()

 

    def __unicode__(self):

        return self.headline

我们以上面的models为例。

I遍历
a = Entry.objects.all()

for e in a:

    print (e.headline)

当遍历一开始时，先从数据库执行查询select * from Entry得到a，然后再遍历a。注意：这里只是查询Entry表，返回的a的每条记录只包含Entry表的字段值，不管Entry的model中是否有onetoone、onetomany、manytomany字段，都不会关联查询。这遵循的是数据库最少读写原则。我们修改一下代码，如下，遍历一开始也是先执行查询得到a，但当执行print (e.blog.name)时，还需要再次查询数据库获取blog实体。

from django.db import connection

l = connection.queries  #l是一个列表，记录SQL语句

a = Entry.objects.all()

for e in a:

    print (e.blog.name)

    len(l)

遍历时，每次都要查询数据库，l长度每次增1，Django提供了方法可以在查询时返回关联表实体，如果是onetoone或onetomany，那用select_related，不过对于onetomany，只能在主表（定义onetomany关系的那个表）的manager中使用select_related方法，即通过select_related获取的关联对象是model instance，而不能是QuerySet，如下，e.blog就是model instance。对于onetomany的反向和manytomany，要用prefetch_related，它返回的是多条关联记录，是QuerySet。

a = Entry.objects.select_related('blog')

for e in a:

        print (e.blog.name)

        len(l)

可以看到从开始到结束，l的长度只增加1。另外，通过查询connection.queries[-1]可以看到Sql语句用了join。

II切片
切片不会立即执行，除非显示指定了步长，如a= Entry.objects.all()[0:10:2]，步长为2。

III序列化，即Pickling
序列化QuerySet很少用

IV repr()
和str()功能相似，将对象转为字符串，很少用。

V len()
计算QuerySet元素的数量，并不推荐使用len()，除非QuerySet是求过值的（即evaluated），否则，用QuerySet.count()获取元素数量，这个效率要高。

VI list()
将QuerySet转为list

VII bool()，判断是否为空
if Entry.objects.filter(headline="Test"):

     print("There is at least one Entry with the headline Test")

 同样不建议这种方法判断是否为空，而应该使用QuerySet.exists()，查询效率高

 

回到顶部
1.2 QuerySet的方法
数据库的常用操作就四种：增、删、改、查，QuerySet的方法涉及删、改、查。后面还会讲model对象的方法，model方法主要是增、删、改、还有调用model实例的字段。

(1) 删delete()
原型：delete()

返回：None

相当于delete-from-where, delete-from-join-where。先filter，然后对得到的QuerySet执行delete()方法就行了，它会同时删除关联它的那些记录，比如我删除记录表1中的A记录，表2中的B记录中有A的外键，那同时也会删除B记录，那ManyToMany关系呢？对于ManyToMany，删除其中一方的记录时，会同时删除中间表的记录，即删除双方的关联关系。由于有些数据库，如Sqlite不支持delete与limit连用，所以在这些数据库对QuerySet的切片执行delete()会出错。如

>>> a = UserEx.objects.filter(is_active=False)

>>> b = a[:3]

>>> b.delete() #执行时会报错

解决：UserEx.objects.filter(pk__in=b).delete() 

in后面可以是一个QuerySet，见 https://docs.djangoproject.com/en/1.6/ref/models/querysets/#in

   

(2) 改 update()
批量修改，返回修改的记录数。不过update()中的键值对的键只能是主表中的字段，不能是关联表字段，如下

Entry.objects.update(blog__name='foo')  #错误，无法修改关联表字段，只能修改Entry表的字段

Entry.objects.filter(blog__name='foo').update(comments_on=False)  #正确

最好的方法是先filter，查询出QuerySet，然后再执行QuerySet.update()。

由于有些数据库，不支持update与limit连用，所以在这些数据库对QuerySet的切片执行update()会出错。

(3)查询 filter(**kwargs)、exclude(**kwargs)、get(**kwargs)
相当于select-from-where，select-from-join-where，很多网站读数据库操作最多。可以看到，filter()的参数是变个数的键值对，而不会出现>,<,!=等符号，这些符号分别用__gt,__lt,~Q或exclude()，不过对于!=，建议使用Q查询，更不容易出错。可以使用双下划线对OneToOne、OneToMany、ManyToMany进行关联查询和反向关联查询，而且方法都是一样的，如：

>>> Entry.objects.filter(blog__name='Beatles Blog') #限定外键表的字段

#下面是反向连接，不过要注意，这里不是entry_set，entry_set是Blog instance的一个属性，代表某个Blog object

#的关联的所有entry，而QuerySet的方法中反向连接是直接用model的小写，不要把两者搞混。It works backwards,

#too. To refer to a “reverse” relationship, just use the lowercase name of the model.

>>> Blog.objects.filter(entry__headline__contains='Lennon')

>>> Blog.objects.filter(entry__authors__name='Lennon')   #ManyToMany关系，反向连接

>>> myblog = Blog.objects.get(id=1)

>>> Entry.objects.filter(blog=myblog)  #正向连接。与下面一句等价，既可以用实体，也可以用

#实体的主键，其实即使用实体，也是只用实体的主键而已。这两种方式对OneToOne、

#OneToMany、ManyToMany的正向、反向连接都适用。

>>> Entry.objects.filter(blog=1)    #我个人不建议这样用，对于create()，不支持这种用法

>>> myentry = Entry.objects.get(id=1)

>>> Blog.objects.filter(entry=myentry) #ManyToMany反向连接。与下面两种方法等价

>>> Blog.objects.filter(entry=1)   

>>> Blog.objects.filter(entry_id=1)  #适用于OneToOne和OneToMany的正向连接

OneToOne的关系也是这样关联查询，可以看到，Django对OneToOne、OneToMany、ManyToMany关联查询及其反向关联查询提供了相同的方式，真是牛逼啊。对于OneToOne、OneToMany的主表，也可以使用下面的方式

Entry.objects.filter(blog_id=1)，因为blog_id是数据库表Entry的一个字段， 这条语句与Entry.objects.filter(blog=blog1)生成的SQL是完全相同的。

 

与filter类似的还有exclude(**kwargs)方法，这个方法是剔除，相当于select-from-where not。可以使用双下划线对OneToOne、OneToMany、ManyToMany进行关联查询和反向关联查询，方法与filter()中的使用方法相同。

>>> Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')

转为SQL为

SELECT *

FROM Entry

WHERE NOT (pub_date > '2005-1-3' AND headline = 'Hello')

 

(4)SQL其它关键字在django中的实现
在SQL中，很多关键词在删、改、查时都是可以用的，如order by、 like、in、join、union、and、or、not等等，我们以查询为例，说一下django如何映射SQL的这些关键字的（查、删、改中这些关键字的使用方法基本相同）。

No1  F类（无对应SQL关键字）
前面提到的filter/exclude中的查询参数值都是常量，如果我们想比较model的两个字段怎么办呢？Django也提供了方法，F类，F类实例化时，参数也可以用双下划线，也可以逻辑运算，如下

>>> from django.db.models import F

>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks'))

>>> from datetime import timedelta

>>> Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))

>>> Entry.objects.filter(authors__name=F('blog__name'))

No2  Q类（对应and/or/not）
如果有or等逻辑关系呢，那就用Q类，filter中的条件可以是Q对象与非Q查询混和使用，但不建议这样做，因为混和查询时Q对象要放前面，这样就有难免忘记顺序而出错，所以如果使用Q对象，那就全部用Q对象。Q对象也很简单，就是把原来filter中的各个条件分别放在一个Q()即可，不过我们还可以使用或与非，分别对应符号为”|”和”&”和”~”，而且这些逻辑操作返回的还是一个Q对象，另外，逗号是各组条件的基本连接符，也是与的关系，其实可以用&代替（在python manage.py shell测试过，&代替逗号，执行的SQL是一样的），不过那样的话可读性会很差，这与我们直接写SQL时，各组条件and时用换行一样，逻辑清晰。

from django.db.models import Q

>>> Poll.objects.get( Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),

question__startswith='Who')   #正确，但不要这样混用

>>> Poll.objects.get( Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),

Q(question__startswith='Who'))  #推荐，全部是Q对象

>>> Poll.objects.get( (Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))&

Q(question__startswith='Who'))  #与上面语句同意，&代替”,”，可读性差

Q类中时应该可以用F类，待测试。

 

No3  annotate（无对应SQL关键字）
函数原型annotate(*args, **kwargs)

返回QuerySet

往每个QuerySet的model instance中加入一个或多个字段，字段值只能是聚合函数，因为使用annotate时，会用group by，所以只能用聚合函数。聚合函数可以像filter那样关联表，即在聚合函数中，Django对OneToOne、OneToMany、ManyToMany关联查询及其反向关联提供了相同的方式，见下面例子。

>>> from django.contrib.auth.models import User

>>> from django.db.models import Count

#计算每个用户的userjob数量，字段命名为ut_num，返回的QuerySet中的每个object都有

#这个字段。在UserJob中定义User为外键，在Job中定义与User是ManyToMany

>>> a = User.objects.filter(is_active=True, userjob__is_active=True). annotate(n=Count(‘userjob’)) #一对多反向连接

>>> b = User.objects.filter(is_active=True, job__is_active=True).annotate(n=Count(‘job__name’))  #多对多反向连接，User与Job是多对多

>>> len(a)  #这里才会对a求值

>>> len(b)  #这里才会对b求值

a对应的SQL语句为(SQL中没有为表起别名,u、ut是我加的)：

select auth.user.*,Count(ut.id) as ut_num

from auth_user as u

left outer join job_userjob as ut on u.id = ut.user_id

where u.is_active=True and ut.is_active=True

group by u.*

 

b对应的SQL语句为(SQL中没有为表起别名,u、t、r是我加的)：

select u.*,Count(t.name) as n

from auth_user as u

left outer join job_job_users as r on u.id=r.user_id

left outer join job_job as t on r.job_id=t.id

where t.is_active=True and u.is_active=True

group by u.*

 

No4  order_by——对应order by
函数原型 order_by(*fields)

返回QuerySet

正向的反向关联表跟filter的方式一样。如果直接用字段名，那就是升序asc排列；如果字段名前加-，就是降序desc

 

No5  distinct——对应distinct
原型 distinct()

一般与values()、values_list()连用，这时它返回ValuesQuerySet、ValuesListQuerySet

这个类跟列表很相似，它的每个元素是一个字典。它没有参数（其实是有参数的，不过，参数只在PostgreSQL上起作用）。使用方法为

>>> a=Author.objects.values_list(name).distinct()

>>> b=Author.objects.values_list(name,email).distinct()

对应的SQL分别为

select distinct name

from Author

和

select distinct name,email

from Author

 

No6  values()和values_list()——对应‘select 某几个字段’
函数原型values(*field), values_list(*field)

返回ValuesQuerySet, ValuesListQuerySet

Author.objects.filter(**kwargs)对应的SQL只返回主表（即Author表）的所有字段值，即使在查询时关联了其它表，关联表的字段也不会返回，只有当我们通过Author instance用关联表时，Django才会再次查询数据库获取值。当我们不用Author instance的方法，且只想返回几个字段时，就要用values()，它返回的是一个ValuesQuerySet对象，它类似于一个列表，不过，它的每个元素是字典。而values_list()跟values()相似，它返回的是一个ValuesListQuerySet，也类型于一个列表，不过它的元素不是字典，而是元组。一般的，当我们不需要model instance的方法且返回多个字段时，用values(*field)，而返回单个字段时用values_list(‘field’,flat=True)，这里flat=True是要求每个元素不是元组，而是单个值，见下面例子。而且我们可以返回关联表的字段，用法跟filter中关联表的方式完全相同。

>>> a = User.objects.values(‘id’,’username’,’userex__age’)

>>> type(a)

<class ‘django.db.models.query.ValuesQuerySet’>

>>> a

[{‘id’:0,’username’:u’test0’,’ userex__age’: 20},{‘id’:1,’username’:u’test1’,’userex__age’: 25},

 {‘id’:2,’username’:u’test2’, ’ userex__age’: 28}]

>>> b= User.objects.values_list(’username’,flat=True)

>>> b

[u’test0’, u’test1’ ,u’test2’]

 

No7  select_related()——对应返回关联记录实体
原型select_related(*filed)

返回QuerySet

它可以指定返回哪些关联表model instance，这里的field跟filter()中的键一样，可以用双下划线，但也有不同，You can refer to any ForeignKey or OneToOneField relation in the list of fields passed to select_related()，QuerySet中的元素中的OneToOne关联及外键对应的是都是关联表的一条记录，如my_entry=Entry.objects.get(id=1)，my_entry.blog就是关联表的一条记录的对象。select_related()不能用于OneToMany的反向连接，和ManyToMany，这些都是model的一条记录对应关联表中的多条记录。前面提到了对于a = Author.objects.filter(**kwargs)这类语句，对应的SQL只返回主表，即Author的所有字段，并不会返回关联表字段值，只有当我们使用关联表时才会再查数据库返回，但有些时候这样做并不好。看下面两段代码，这两段代码在1.1中提到过。在代码1中，在遍历a前，先执行a对应的SQL，拿到数据后，然后再遍历a，而遍历过程中，每次都还要查询数据库获取关联表。代码2中，当遍历开始前，先拿到Entry的QuerySet，并且也拿到这个QuerySet的每个object中的blog对象，这样遍历过程中，就不用再查询数据库了，这样就减少了数据库读次数。

代码1

a = Entry.objects.all()

for e in a:

    print (e.blog.name)

 

代码2

a = Entry.objects.select_related('blog')

for e in a:

        print (e.blog.name)

No8  prefetch_related(*field) ——对应返回关联记录实体的集合
函数原型prefetch_related(*field)

返回的是QuerySet

这里的field跟filter()中的键一样，可以用双下划线。用于OneToMany的反向连接，及ManyToMany。其实，prefetch_related()也能做select_related()的事情，但由于策略不同，可能相比select_related()要低效一些，所以建议还是各管各擅长的。select_related是用select ……join来返回关联的表字段，而prefetch_related是用多条SQL语句的形式查询，一般，后一条语句用IN来调用上一句话返回的结果。

class Restaurant(models.Model):

    pizzas = models.ManyToMany(Pizza, related_name='restaurants')

    best_pizza = models.ForeignKey(Pizza, related_name='championed_by')

 

>>> Restaurant.objects.prefetch_related('pizzas__toppings')

>>> Restaurant.objects.select_related('best_pizza').prefetch_related('best_pizza__toppings')

先用select_related查到best_pizza对象，再用prefetch_related 从best_pizza查出toppings

 

No9  extra()——实现复杂的where子句
函数原型：extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None)

基本上，查询时用django提供的方法就够用了，不过有时where子句中包含复杂的逻辑，这种情况下django提供的方法可能不容易做到，还好，django有extra()， extra()中直接写一些SQL语句。不过，不同的数据库用的SQL有些差异，所以尽可能不要用extra()。需要时再看使用方法吧。

 

No10  aggregate(*args, **kwargs)——对应聚合函数
参数为聚合函数，最好用**kwargs的形式，每个参数起一个名字。

该函数与annotate()有何区别呢？annotate相当于aggregate()和group by的结合，对每个group执行aggregate()函数。而单独的aggregate()并没有group by。

 

>>> from django.db.models import Count

>>> q = Blog.objects.aggregate(Count('entry'))  #这是用*args的形式，最好不要这样用

>>> q = Blog.objects.aggregate(number_of_entries=Count('entry'))  #这是用**kwargs的形式

{'number_of_entries': 16}

 

    至此，我们总结了QuerySet方法返回的数据形式，主要有五种。第一种：返回QuerySet，每个object只包含主表字段；第二种：返回QuerySet，每个object除了包含主表所有字段，还包含某些关联表的object，这种情况要用select_related()和prefetch_related()，可以是任意深度（即任意多个双下划线）的关联，通常一层关联和二层关联用的比较多；第三种：返回ValuesQuerySet, ValuesListQuerySet，它们的每个元素包含若干主表和关联表的字段，不包含任何实体和关联实例，这种情况要用values()和values_list()；第四种：返回model instance；第五种:单个值，如aggregate()方法。

 

 

No11  exists()、count()、len()
如果只是想知道一个QuerySet是否为空，而不想获取QuerySet中的每个元素，那就用exists()，它要比len()、count()、和直接进行if判断效率高。如果只想知道一个QuerySet有多大，而不想获取QuerySet中的每个元素，那就用count()；如果已经从数据库获取到了QuerySet，那就用len()

 

No12  contains/startswith/endswith——对应like
    字段名加双下划线，除了它，还有icontains，即Case-insensitive contains，这个是大小写不敏感的，这需要相应数据库的支持。有些数据库需要设置

才能支持大小写敏感。

No13  in——对应in
字段名加双下划线

 

No14 exclude(field__in=iterable)——对应not in
iterable是可迭代对象

 

 

 

No15  gt/gte/lt/lte——对应于>,>=,<,<=
字段名加双下划线

No16  range——对应于between and
字段名加双下划线，range后面值是列表

No17  isnull——对应于is null
Entry.objects.filter(pub_date__isnull=True)对应的SQL为SELECT ... WHERE pub_date IS NULL;

No18  QuerySet切片——对应于limit
    QuerySet的索引只能是非负整数，不支持负整数，所以QuerySet[-1]错误

a=Entry.objects.all()[5:10]

b=len(a) 

执行Entry.objects.all()[5:8]，对于不同的数据库，SQL语句不同，Sqlite 的SQL语句为select * from tablename limit 3 offset 5; MySQL的SQL语句为select * from tablename limit 5,3

 

参考资料：

    1、https://docs.djangoproject.com/en/1.6/ref/models/querysets/

    2、https://docs.djangoproject.com/en/1.6/topics/db/queries/
```
