---
layout:post
title:@classmethod与@staticmethod的区别与用途
date:2018-02-24
author:muyalei
tags:
    - python笔记
---

转自[http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/](http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/)

### 个人总结：
>@classmethod修饰类中定义的方法，使得这个方法只与类交互而不与实例交互，即：默认下，类中定义的方法的第一个参数self指向实例，而经过@classmethod修饰的方法的self参数指向类本身，无论是通过类调用还是通过实例调用这个方法，self参数都指向类本身。</br>
类似于类中定义的属于类的参数和属于实例的参数(def __init__(self,a,b)这里的a,b参数属于实例)，被@classmethod修饰后的方法属于类，任何实例都可以访问但是不能修改。可以使用类提供的参数，不能使用实例提供的参数。</br>
@staticmethod 修饰类中定义的方法，但是这个方法跟这个类无关，这个类不能使用实例或类提供的参数，只是一个与当前类无关的一个函数。比如根据环境变量做判断的一个函数，这个函数与类有关系，但是类或实例不能操作这个函数，就可以用@staticmethod。可以认为是，一个本该在类外面的函数，与这个类还有点关系，为了代码统一方便后续维护而将这个函数通过@staticmethod这么一个方法放在了类中。
区别：
     
 

图解:   






区别：
作者：fosmjo
链接：https://www.zhihu.com/question/20021164/answer/42704772
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
看了很多解释,感觉还是这个比较清楚
oop - Python @classmethod and @staticmethod for beginner?
@classmethod means: when this method is called, we pass the class as the first argument instead of the instance of that class (as we normally do with methods). This means you can use the class and its properties inside that method rather than a particular instance.
@staticmethod means: when this method is called, we don't pass an instance of the class to it (as we normally do with methods). This means you can put a function inside a class but you can't access the instance of that class (this is useful when your method does not use the instance).

用途：

Class vs static methods in Python
In this article I'll try to explain what are staticmethod and classmethod, and what the difference is between them. staticmethod and classmethod both use decorators for defining a method as a staticmethod or classmethod. Please take a look at the article Python Decorators Overview for a basic understanding of how decorators works in Python.
Simple, static and class methods
The most used methods in classes are instance methods, i.e instance is passed as the first argument to the method.
For example, a basic instance method would be as follows:

class Kls(object)：
def __init__(self,data):
    self.data = data
	def printd(self):
       print(self.data)
ik1 = Kls(‘arun’)
ik2 = Kls(‘seema’)
ik1.printd()
ik2.printd()
This gives us the following output:
1
2	arun
seema
 
After looking at the code sample and diagram:
•	In 1 and 2, the arguments are passed to the method.
•	On 3, the self argument refers to the instance.
•	At 4, we do not need to provide the instance to the method, as it is handled by the interpretor itself.
Now what if the method we want to write interacts with classes only and not instances? We can code a simple function out of the class to do so but that will spread the code related to class, to out of the class. This can cause a future code maintenance problem, as follows:
1
2
3
4
5
6
7
8
9
10
11
12
13	def get_no_of_instances(cls_obj):
    return cls_obj.no_inst
 
class Kls(object):
    no_inst = 0
 
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
 
ik1 = Kls()
ik2 = Kls()
 
print(get_no_of_instances(Kls))
Gives us the following output:
1	2
The Python @classmethod
What we want to do now is create a function in a class, which gets the class object to work on instead of the instance. If we want to get the no of instances, all we have to do is something like below:
1
2
3
4
5
6
7
8
9
10
11
12	def iget_no_of_instance(ins_obj):
    return ins_obj.__class__.no_inst
 
class Kls(object):
    no_inst = 0
 
    def __init__(self):
    Kls.no_inst = Kls.no_inst + 1
 
ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)
 
1	2
Using features introduced after Python 2.2, we can create a method in a class, using @classmethod.
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15	class Kls(object):
    no_inst = 0
 
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
 
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst
 
ik1 = Kls()
ik2 = Kls()
 
print ik1.get_no_of_instance()
print Kls.get_no_of_instance()
We get the following output:
1
2	2
2
The benefit of this is: whether we call the method from the instance or the class, it passes the class as first argument.
The Python @staticmethod
Often there is some functionality that relates to the class, but does not need the class or any instance(s) to do some work. Perhaps something like setting environmental variables, changing an attribute in another class, etc. In these situation we can also use a function, however doing so also spreads the interrelated code which can cause maintenance issues later.
This is a sample case:
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21	IND = 'ON'
 
def checkind():
    return (IND == 'ON')
 
class Kls(object):
     def __init__(self,data):
        self.data = data
 
def do_reset(self):
    if checkind():
        print('Reset done for:', self.data)
 
def set_db(self):
    if checkind():
        self.db = 'new db connection'
        print('DB connection made for:',self.data)
 
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
Which gives us the following output:
1
2	Reset done for: 12
DB connection made for: 12
Here if we use a @staticmethod, we can place all code in the relevant place.
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22	IND = 'ON'
 
class Kls(object):
    def __init__(self, data):
        self.data = data
 
    @staticmethod
    def checkind():
        return (IND == 'ON')
 
    def do_reset(self):
        if self.checkind():
            print('Reset done for:', self.data)
 
    def set_db(self):
        if self.checkind():
            self.db = 'New db connection'
        print('DB connection made for: ', self.data)
 
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
Which gives us the following output:
1
2	Reset done for: 12
DB connection made for: 12
Here is a more comprehensive code example, with a diagram to show you
How @staticmethod and @classmethod are different.
1
2
3
4
5
6
7
8
9
10
11
12
13
14	class Kls(object):
    def __init__(self, data):
        self.data = data
 
    def printd(self):
        print(self.data)
 
    @staticmethod
        def smethod(*arg):
            print('Static:', arg)
 
    @classmethod
        def cmethod(*arg):
            print('Class:', arg)
1
2
3
4
5
6
7
8
9
10
11
12
13	>>> ik = Kls(23)
>>> ik.printd()
23
>>> ik.smethod()
Static: ()
>>> ik.cmethod()
Class: (<class '__main__.Kls'>,)
>>> Kls.printd()
TypeError: unbound method printd() must be called with Kls instance as first argument (got nothing instead)
>>> Kls.smethod()
Static: ()
>>> Kls.cmethod()
Class: (<class '__main__.Kls'>,)
Here's a diagram to explain what's going on:
 
译文：
作者：李保银
链接：https://www.zhihu.com/question/20021164/answer/18224953
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
普通方法，静态方法和类方法 
这个答案的原文是Difference between @staticmethod and @classmethod in Python
这里的内容是我通知原作者并得到允许的情况下的翻译稿
这个是我的博客文章的地址pyhton静态方法和类方法
类中最常用的方法是实例方法, 即通过通过实例作为第一个参数的方法。
举个例子，一个基本的实例方法就向下面这个:
 
class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
ik1 = Kls('arun')
ik2 = Kls('seema')
ik1.printd()
ik2.printd()

这会给出如下的输出:
arun
seema
&lt;img src="https://pic4.zhimg.com/a2173bce20299607befc10abf8c7041b_b.jpg" data-rawwidth="372" data-rawheight="322" class="content_image" width="372"&gt; 

然后看一下代码和示例图片:
•	1，2参数传递给方法.
•	3 self参数指向当前实例自身.
•	4 我们不需要传递实例自身给方法，Python解释器自己会做这些操作的.
如果现在我们想写一些仅仅与类交互而不是和实例交互的方法会怎么样呢? 我们可以在类外面写一个简单的方法来做这些，但是这样做就扩散了类代码的关系到类定义的外面. 如果像下面这样写就会导致以后代码维护的困难:
 
def get_no_of_instances(cls_obj):
    return cls_obj.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print(get_no_of_instances(Kls))

输出:
2
@classmethod
我们要写一个只在类中运行而不在实例中运行的方法. 如果我们想让方法不在实例中运行，可以这么做:
 
def iget_no_of_instance(ins_obj):
    return ins_obj.__class__.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
    Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)

输出
2
在Python2.2以后可以使用@classmethod装饰器来创建类方法.
 
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst
ik1 = Kls()
ik2 = Kls()
print ik1.get_no_of_instance()
print Kls.get_no_of_instance()

输出:
2
2
这样的好处是: 不管这个方式是从实例调用还是从类调用，它都用第一个参数把类传递过来.
@staticmethod
经常有一些跟类有关系的功能但在运行时又不需要实例和类参与的情况下需要用到静态方法. 比如更改环境变量或者修改其他类的属性等能用到静态方法. 这种情况可以直接用函数解决, 但这样同样会扩散类内部的代码，造成维护困难.
比如这样:
 
IND = 'ON'
def checkind():
    return (IND == 'ON')
class Kls(object):
     def __init__(self,data):
        self.data = data
def do_reset(self):
    if checkind():
        print('Reset done for:', self.data)
def set_db(self):
    if checkind():
        self.db = 'new db connection'
        print('DB connection made for:',self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()

输出:
Reset done for: 12
DB connection made for: 12
如果使用@staticmethod就能把相关的代码放到对应的位置了.
 
IND = 'ON'
class Kls(object):
    def __init__(self, data):
        self.data = data
    @staticmethod
    def checkind():
        return (IND == 'ON')
    def do_reset(self):
        if self.checkind():
            print('Reset done for:', self.data)
    def set_db(self):
        if self.checkind():
            self.db = 'New db connection'
        print('DB connection made for: ', self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()

输出:
Reset done for: 12
DB connection made for: 12
下面这个更全面的代码和图示来展示这两种方法的不同
@staticmethod 和 @classmethod的不同
 
class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
    @staticmethod
    def smethod(*arg):
        print('Static:', arg)
    @classmethod
    def cmethod(*arg):
        print('Class:', arg)
 
>>> ik = Kls(23)
>>> ik.printd()
23
>>> ik.smethod()
Static: ()
>>> ik.cmethod()
Class: (<class '__main__.Kls'>,)
>>> Kls.printd()
TypeError: unbound method printd() must be called with Kls instance as first argument (got nothing instead)
>>> Kls.smethod()
Static: ()
>>> Kls.cmethod()
Class: (<class '__main__.Kls'>,)

下面这个图解释了以上代码是怎么运行的:
&lt;img src="https://pic3.zhimg.com/8a82a7f295c855c39b0d21f5bb1352c2_b.jpg" data-rawwidth="563" data-rawheight="324" class="origin_image zh-lightbox-thumb" width="563" data-original="https://pic3.zhimg.com/8a82a7f295c855c39b0d21f5bb1352c2_r.jpg"&gt; 
编辑于 2015-08-13




