---
layout: default
author: muyalei
date: 2018-05-19
title: Django Models的数据类型
tags:
   - django
---

***转载自[http://www.cnblogs.com/zknublx/p/5944779.html](http://www.cnblogs.com/zknublx/p/5944779.html)***

## Django中的页面管理后台
Djano中自带admin后台管理模块,可以通过web页面去管理,有点想php-admin,使用步骤:

1. 在项目中models.py 中创建数据库表
```
class userinfo(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    email = models.EmailField()
    ip = models.GenericIPAddressField()
    memo = models.TextField()
    img = models.ImageField()
    usertype=models.ForeignKey("usertype",null=True,blank=True)

class usertype(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
```
2. 在terminal中执行
```
python manage.py makemigrations
   python manage.py migrate

#创建超级用户,设置管理员密码,密码至少8位
   python manage.py createsuperuser
```
3. 在项目中的admin.py中设置,注册已经设置的数据库
```
from django.contrib import admin

# Register your models here.

from app01 import models
admin.site.register(models.userinfo)
admin.site.register(models.usertype)
```
4. 在页面中访问/admin,即可访问后台管理以及对数据增删改查

## model详解
Django中遵循 Code Frist 的原则，即：根据代码中定义的类来自动生成数据库表。

### 创建表
#### 基本结构
```
from django.db import models

# Create your models here.

class userinfo(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    email = models.EmailField()
    ip = models.GenericIPAddressField()
    memo = models.TextField()
    img = models.ImageField()
    usertype=models.ForeignKey("usertype",null=True,blank=True)

class usertype(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
```
更多字段:
```
1、models.AutoField　　自增列 = int(11)
　　如果没有的话，默认会生成一个名称为 id 的列，如果要显示的自定义一个自增列，必须将给列设置为主键 primary_key=True。
2、models.CharField　　字符串字段
　　必须 max_length 参数
3、models.BooleanField　　布尔类型=tinyint(1)
　　不能为空，Blank=True
4、models.ComaSeparatedIntegerField　　用逗号分割的数字=varchar
　　继承CharField，所以必须 max_lenght 参数
5、models.DateField　　日期类型 date
　　对于参数，auto_now = True 则每次更新都会更新这个时间；auto_now_add 则只是第一次创建添加，之后的更新不再改变。
6、models.DateTimeField　　日期类型 datetime
　　同DateField的参数
7、models.Decimal　　十进制小数类型 = decimal
　　必须指定整数位max_digits和小数位decimal_places
8、models.EmailField　　字符串类型（正则表达式邮箱） =varchar
　　对字符串进行正则表达式
9、models.FloatField　　浮点类型 = double
10、models.IntegerField　　整形
11、models.BigIntegerField　　长整形
　　integer_field_ranges = {
　　　　'SmallIntegerField': (-32768, 32767),
　　　　'IntegerField': (-2147483648, 2147483647),
　　　　'BigIntegerField': (-9223372036854775808, 9223372036854775807),
　　　　'PositiveSmallIntegerField': (0, 32767),
　　　　'PositiveIntegerField': (0, 2147483647),
　　}
12、models.IPAddressField　　字符串类型（ip4正则表达式）
13、models.GenericIPAddressField　　字符串类型（ip4和ip6是可选的）
　　参数protocol可以是：both、ipv4、ipv6
　　验证时，会根据设置报错
14、models.NullBooleanField　　允许为空的布尔类型
15、models.PositiveIntegerFiel　　正Integer
16、models.PositiveSmallIntegerField　　正smallInteger
17、models.SlugField　　减号、下划线、字母、数字
18、models.SmallIntegerField　　数字
　　数据库中的字段有：tinyint、smallint、int、bigint
19、models.TextField　　字符串=longtext
20、models.TimeField　　时间 HH:MM[:ss[.uuuuuu]]
21、models.URLField　　字符串，地址正则表达式
22、models.BinaryField　　二进制
23、models.ImageField   图片
24、models.FilePathField 文件
```
更多参数:
```
1、null=True
　　数据库中字段是否可以为空
2、blank=True
　　django的 Admin 中添加数据时是否可允许空值
3、primary_key = False
　　主键，对AutoField设置主键后，就会代替原来的自增 id 列
4、auto_now 和 auto_now_add
　　auto_now   自动创建---无论添加或修改，都是当前操作的时间
　　auto_now_add  自动创建---永远是创建时的时间
5、choices
GENDER_CHOICE = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
gender = models.CharField(max_length=2,choices = GENDER_CHOICE)
6、max_length
7、default　　默认值
8、verbose_name　　Admin中字段的显示名称
9、name|db_column　　数据库中的字段名称
10、unique=True　　不允许重复
11、db_index = True　　数据库索引
12、editable=True　　在Admin里是否可编辑
13、error_messages=None　　错误提示
14、auto_created=False　　自动创建
15、help_text　　在Admin中提示帮助信息
16、validators=[]
17、upload-to   上传到哪个位置,更多与image,filepath配合使用
```

#### 连表结构
1. 一对多:models.ForeignKey(其他表)
2. 多对多:models.ManyToManyField(其他表)
3. 一对一:models.ManyToManyField(其他表)

*应用场景:*

- 一对多：当一张表中创建一行数据时，有一个单选的下拉框（可以被重复选择）

  例如：创建用户信息时候，需要选择一个用户类型【普通用户】【金牌用户】【铂金用户】等。

- 多对多：在某表中创建一行数据是，有一个可以多选的下拉框

  例如：创建用户信息，需要为用户指定多个爱好

- 一对一：在某表中创建一行数据时，有一个单选的下拉框（下拉框中的内容被用过一次就消失了

  例如：原有含10列数据的一张表保存相关信息，经过一段时间之后，10列无法满足需求，需要为原来的表再添加5列数据

看个例子:
```
from django.db import models

# Create your models here.
from django.db import models

# 陈超，普通用户
# 淮军，超级用户
class Gender(models.Model):
    name = models.CharField(max_length=32)


class userinfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='用户名',editable=False)
    email = models.EmailField(db_index=True)
    memo = models.TextField()
    img = models.ImageField(upload_to='upload')
    user_type = models.ForeignKey("UserType", null=True, blank=True)# unique
    # user_type = models.OneToOneField("UserType", null=True, blank=True)# unique
    # ctime = models.DateTimeField(auto_now_add=True)
    # uptime = models.DateTimeField(auto_now=True)

    # gender = models.ForeignKey(Gender)
    gender_choices = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(choices=gender_choices,default=1)

# 普通用户，超级用户
class UserType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class B2G(models.Model):
    boy = models.ForeignKey('Boy')
    girl = models.ForeignKey('Girl')

class Boy(models.Model):
    name = models.CharField(max_length=32)
# 吴文煜，王建，王志刚，杜宝强

class Girl(models.Model):
    name = models.CharField(max_length=32)

    f = models.ManyToManyField(Boy)
# 铁锤，钢弹，如花
```




#### TIPS:
1. modles.py中class设置的数据,本身返回为一个类,如果想直接返回某一个字段的值,可以定义`__str__`,比如:
```
class TypeUser(models.Model):
    name = models.CharFiled(max_length=32)
    def __str__(self):
        return self.name
```

2. 在设置ForeignKey时,参数中的第一个参数为表名,\*\*需要注意的是,加不加引号有区别:加引号后表的定义顺序可以随便,但不加引号必须按照顺序来:
```
class userinfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='用户名',editable=False)
    email = models.EmailField(db_index=True)
    memo = models.TextField()
    img = models.ImageField(upload_to='upload')
    user_type = models.ForeignKey("UserType", null=True, blank=True)# unique
    # user_type = models.OneToOneField("UserType", null=True, blank=True)# unique
    # ctime = models.DateTimeField(auto_now_add=True)
    # uptime = models.DateTimeField(auto_now=True)

    # gender = models.ForeignKey(Gender)
    gender_choices = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(choices=gender_choices,default=1)

class UserType(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
```
3. 多对多,有两种创建方式

   1. 自建第三张表
   
   2. 自动创建,比如:
      ```
      #自建第三张表
      class B2G(models.Model):
          boy = models.ForeignKey('Boy')
          girl = models.ForeignKey('Girl')

      class Boy(models.Model):
          name = models.CharField(max_length=32)
          # 吴文煜，王建，王志刚，杜宝强

      class Girl(models.Model):
          name = models.CharField(max_length=32)
          #自动创建
          f = models.ManyToManyField(Boy)
      ```

多对多详情参考：[http://www.cnblogs.com/zknublx/p/5959295.html](http://www.cnblogs.com/zknublx/p/5959295.html)

4. queryset

从数据库中提取出来的数据为queryset类型,是Django中的一种特殊类型.
```
w = models.Simp.objects.all()
print(w, type(w))
[<Simp: chenc>, <Simp: zan>, <Simp: zhangsan>]<class 'django.db.models.query.QuerySet'>
```
可以看到，从数据库取出个数据看起来像包含对象的列表。而实际上整个数据为django中的特殊类型QuerySet。

如果需要查看原来的SQL语句,可以使用`queryset.query`:

`print(w.query)`

5. values() 和 vlue_list() 与 all()区别

.all()是取得所有列的数据，可以加.values()取出某一列，每一个元素为一个字典：
```
obj = model.UserInfo.objects.filter(name='alex').values('id','email')
# select id from userinfo where name = 'alex'

queryset -> python，Django的类
[{'id':1},{'id': 2},]
```
values_list()，获取到的元素为一个个元组,也可以加多个参数来获取多列:
```
obj = model.UserInfo.objects.filter(name='alex').value_list('id','email')
# select id from userinfo where name = 'alex'

queryset -> python，Django的类
[(1,'1@qq.com'),(2,'alex@11.com'),]
```

### 表操作
#### 基本操作
```
# 增
    #
    # models.Tb1.objects.create(c1='xx', c2='oo')  增加一条数据，可以接受字典类型数据 **kwargs

    # obj = models.Tb1(c1='xx', c2='oo')
    # obj.save()

    # 查
    #
    # models.Tb1.objects.get(id=123)         # 获取单条数据，不存在则报错（不建议）
    # models.Tb1.objects.all()               # 获取全部
    # models.Tb1.objects.filter(name='seven') # 获取指定条件的数据

    # 删
    #
    # models.Tb1.objects.filter(name='seven').delete() # 删除指定条件的数据

    # 改
    # models.Tb1.objects.filter(name='seven').update(gender='0')  # 将指定条件的数据更新，均支持 **kwargs
    # obj = models.Tb1.objects.get(id=1)
    # obj.c1 = '111'
    # obj.save()                                                 # 修改单条数据
```

#### 进阶操作(了不起的双下划线)
利用双下划线将字段和对应的操作连接起来
```
# 获取个数
    #
    # models.Tb1.objects.filter(name='seven').count()

    # 大于，小于
    #
    # models.Tb1.objects.filter(id__gt=1)              # 获取id大于1的值
    # models.Tb1.objects.filter(id__lt=10)             # 获取id小于10的值
    # models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值

    # in
    #
    # models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
    # models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in

    # contains
    #
    # models.Tb1.objects.filter(name__contains="ven")
    # models.Tb1.objects.filter(name__icontains="ven") # icontains大小写不敏感
    # models.Tb1.objects.exclude(name__icontains="ven")

    # range
    #
    # models.Tb1.objects.filter(id__range=[1, 2])   # 范围bettwen and

    # 其他类似
    #
    # startswith，istartswith, endswith, iendswith,

    # order by
    #
    # models.Tb1.objects.filter(name='seven').order_by('id')    # asc
    # models.Tb1.objects.filter(name='seven').order_by('-id')   # desc

    # limit 、offset
    #
    # models.Tb1.objects.all()[10:20]

    # group by
    from django.db.models import Count, Min, Max, Sum
    # models.Tb1.objects.filter(c1=1).values('id').annotate(c=Count('num'))
    # SELECT "app01_tb1"."id", COUNT("app01_tb1"."num") AS "c" FROM "app01_tb1" WHERE "app01_tb1"."c1" = 1 GROUP BY "app01_tb1"."id"
```




#### 连表操作(了不起的双下划线)
利用双下划线和` _set `将表之间的操作连接起来

数据库表结构:
```
class UserProfile(models.Model):
    user_info = models.OneToOneField('UserInfo')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __unicode__(self):
        return self.username


class UserInfo(models.Model):
    user_type_choice = (
        (0, u'普通用户'),
        (1, u'高级用户'),
    )
    user_type = models.IntegerField(choices=user_type_choice)
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    address = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class UserGroup(models.Model):

    caption = models.CharField(max_length=64)

    user_info = models.ManyToManyField('UserInfo')

    def __unicode__(self):
        return self.caption


class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()
    user_group = models.ForeignKey('UserGroup')

    def __unicode__(self):
        return self.hostname
```
一对一操作:
```
user_info_obj = models.UserInfo.objects.filter(id=1).first()
print user_info_obj.user_type
print user_info_obj.get_user_type_display()
print user_info_obj.userprofile.password
 
user_info_obj = models.UserInfo.objects.filter(id=1).values('email', 'userprofile__username').first()
print user_info_obj.keys()
print user_info_obj.values()
```
一对多操作,类似于一对一:

1、搜索条件使用 __ 连接

2、获取值时使用 .    连接

多对多操作:
```
user_info_obj = models.UserInfo.objects.get(name=u'武沛齐')
user_info_objs = models.UserInfo.objects.all()
 
group_obj = models.UserGroup.objects.get(caption='CEO')
group_objs = models.UserGroup.objects.all()
 
# 添加数据
#group_obj.user_info.add(user_info_obj)
#group_obj.user_info.add(*user_info_objs)
 
# 删除数据
#group_obj.user_info.remove(user_info_obj)
#group_obj.user_info.remove(*user_info_objs)
 
# 添加数据
#user_info_obj.usergroup_set.add(group_obj)
#user_info_obj.usergroup_set.add(*group_objs)
 
# 删除数据
#user_info_obj.usergroup_set.remove(group_obj)
#user_info_obj.usergroup_set.remove(*group_objs)
 
# 获取数据
#print group_obj.user_info.all()
#print group_obj.user_info.all().filter(id=1)
 
# 获取数据
#print user_info_obj.usergroup_set.all()
#print user_info_obj.usergroup_set.all().filter(caption='CEO')
#print user_info_obj.usergroup_set.all().filter(caption='DBA')
```

其他操作:
```
# F 使用查询条件的值
    #
    # from django.db.models import F
    # models.Tb1.objects.update(num=F('num')+1)

    # Q 构建搜索条件
    from django.db.models import Q
    # con = Q()
    #
    # q1 = Q()
    # q1.connector = 'OR'
    # q1.children.append(('id', 1))
    # q1.children.append(('id', 10))
    # q1.children.append(('id', 9))
    #
    # q2 = Q()
    # q2.connector = 'OR'
    # q2.children.append(('c1', 1))
    # q2.children.append(('c1', 10))
    # q2.children.append(('c1', 9))
    #
    # con.add(q1, 'AND')
    # con.add(q2, 'AND')
    #
    # models.Tb1.objects.filter(con)

    #
    # from django.db import connection
    # cursor = connection.cursor()
    # cursor.execute("""SELECT * from tb where name = %s""", ['Lennon'])
    # row = cursor.fetchone()
```
**xx_set中的`_set`是多对多的固定搭配**





### 扩展
#### 自定义上传
```
def upload_file(request):
    if request.method == "POST":
        obj = request.FILES.get('fafafa')
        f = open(obj.name, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
    return render(request, 'file.html')
```
form上传文件实例
```
class FileForm(forms.Form):
    ExcelFile = forms.FileField()
```
models.py:
```
from django.db import models

class UploadFile(models.Model):
    userid = models.CharField(max_length = 30)
    file = models.FileField(upload_to = './upload/')
    date = models.DateTimeField(auto_now_add=True)
```
view.py:
```
def UploadFile(request):
    uf = AssetForm.FileForm(request.POST,request.FILES)
    if uf.is_valid():
            upload = models.UploadFile()
            upload.userid = 1
            upload.file = uf.cleaned_data['ExcelFile']
            upload.save()
            
            print upload.file
```
