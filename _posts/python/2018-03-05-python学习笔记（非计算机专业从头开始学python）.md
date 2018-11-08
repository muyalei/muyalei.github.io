---
layout:     post
title:      python学习及使用中遇到的问题总结（非计算机专业从头开始学Python）
subtitle:   学习笔记
date:       2018-02-09
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - 学习笔记
    - 基础知识
---

#### 写在前面
>跨专业进入IT领域，一步一步走到现在，目前算是个及格的爬虫工程师，下面是我学习过程中遇到的问题（可惜还有好些坑没能记录下来），记录下来，以便随时查看。

1. urlopen抓取到的是一个HTTPResponse对象，可以使用.read()方法读取成一个bytes对象

2. bsobj = BeautifulSoup(html)
   创建的bsobj是一个bs4.BeautifulSoup对象，是对html对象的解析；
   bsobj.findAll()得到的是一个bs4.element.ResultSet对象，是一个list，可以通过.get_text()获取字符串内容;
   bsobj.findAll()[0]或者bsobj.find()的得到的是一个bs4.element.Tag对象，可以继续对该对象使用findAll方法，得到的结果
   仍然是bs4.element.Tag对象，使用.text获取字符串内容；
   ResultSet对象可以使用get_text()方法直接获取去除Tag标签后的文本内容，返回结果是一个str对象；
   findAll方法返回的Resultset对象是一个list，是一个可迭代对象，多用来进行迭代；而find方法返回的Tag对象可以层层
   定位目标节点，并可以使用get_text()方法获取文本内容；
   bs4.element.Tag抓取指定的标签的属性，如抓取标签属性中的连接地址，可以使用 .attrs["href"]的方法，抓取到href属性
   的值；
   findAll方法拿到的结果被遍历的时候，遍历出来的每个元素仍然可以使用find()方法查找目标节点；
   
3. 字符编码问题：
   str对象通过encode编码成bytes对象，如'a'.encode('utf-8'),bytes对象通过decode解码成str对象，
   如b'\xa420'.decode('utf-8')；
   'a'.encode('utf-8')是将str对象'a'编码，bytes(str,'utf-8')是调用类bytes创建bytes实例对象，
   二者等价；
   b'\xa420'.decode('utf-8')是解码，str(bytes,'utf-8')是创建str对象；
   encode、encoding区别：
   encode是对str对象进行编码，使用方式是str.encode("utf-8"),
   encoding是对response对象进行编码，使用方式是response.encoding="utf-8"，需要注意，str对象没有encoding方法;

4. 查找子标签、兄弟标签(next_siblings)，只能使用bsobj.find(--).children，不能
   使用bsobj.findAll(--).children；
   逐层过滤标签时，bsobj.find(--).findAll(--)是正确的，不能使用bsobj.findAll(--).findAll(--)

5. pickle序列化：
   pickle.dumps(d)将可以是任意对象的序列化成bytes对象，如a=pickle.dumps(--)，之后可以对a进行写入文件等操作，
   如直接使用with open(--) as f 写入文件；
   pickle.dump(d,f)需要先f=open(r"--","wb")打开一个文件对象，之后pick.dump(d,f)直接将序列化后
   的bytes对象写入文件，调用f.close()关闭文件；
   反序列化：
   内存中序列化的对象反序列化，直接使用pick.loads(a)；
   磁盘上保存的序列化后的文件反序列化进内存，首先f=open(r"--\test.txt","rb")打开需要反序列化的
   目标文件，然后d=pickle.load(f)进行反序列化，最后f.close()；
   注意：向文件写入bytes对象时，要用"wb"，没有errors参数；
   json序列化与pickle用法相同，区别是json序列化后生成对象是 str对象。

6. scrapy下xpath、css选取节点
   html = "<html class="red"><body><span>good!</span></body></html>",
   response.xpath('//html[@class="red"]').extract()，表示获取class属性值是red的所有html节点及其
   子节点，结果是['<html class-->....</html>']，返回的是一个list；
   response.xpath('//base/@href').extract()，全局获取base标签下的href属性的值；

7. 1)StringIO实现在内存中读写str，(相对应于直接读写文件中数据)，通过f=StringIO()创建一个StringIO对象f，
   f.write('Hello world')将数据写入f，使用f.read()或f.getvalue()方法读取f数据；
   2)使字符串具有文件属性，也可以直接使用字符串初始化StringIO，形如StringIO('abc')，在内存中使str对象具有文件的属性，可以像对待文件对象一样读写，
   结果是让Python把StringIO处理后的字符串当成文件来处理，可以使用read()或getvalue()方法读取；
   BytesIO(bytes对象)，接受一个二进制对象，与StringIO用法一样，StringIO处理str对象，BytesIO处理bytes对象；

8. sys.argv包含了命令行参数的列表，即从程序外面使用命令行给程序传递参数；
   python test.py we are arguments，使用python执行test.py程序，sys.argv[1:]表示["we","are","arguments"]
   这个list，test.py程序本身永远是sys.argv[0]; 

9. python的私有变量,如:
   ```
   def Student(object):
       def __init__(self,name,score):
           self.__name = name
	   self.__score = score
   ```
   这样设置后，只有在将类实例化的时候，如Bob=Student("Bob",99)，私有属性self.__name会被设置一次，之后
   不能通过xx.__name的形式读取或者写入该变量的值。要访问变量的值，要么使用Bob=Student("Bobey",88)这样
   再重新实例化一次，要么
   def get_score(self): => return self.__score 读变量
   def set_score(self,score): => return self.__score = score 写变量

10. 继承与多态                                           
    ```
    class Animal(object):                   class Dog(Animal):     class Dog(Animal):
        def run(self):                          pass                   def run(self):
            print("Animal is running")                                     print("dog is running...")
----------------------------------------
    def run_twice(animal):
        animal.run()
        animal.run()
    ```
    父类是Animal的类，都继承了run()方法，所以只要是Animal的子类都具有run()方法，都可以直接作为
    run_twice()函数的参数，run()方法具体作用在Animal身上还是Dog身上，就看子类Dog有没有自定义run()方法，
    子类的run()方法默认覆盖父类。(甚至不必是Animal的子类，只要某个类或实例有一个run()方法，都可以)

11. 判断对象属性
    hasattr(obj,"read") obj对象是否存在read属性？
    getattr(obj,"score",[,00]) 获取对象score属性，若属性不存在则返回00，默认返回值是可选参数
    setattr(obj,"score",99) 将obj对象score属性设置为99；

12. 装饰器@property用在类中定义了私有变量的情况下，要访问私有变量，只能通过定义方法get_score/set_score，
    @property用来简化这个过程，@property用来在类中装饰方法函数，比如get_score()装饰成score，并生成一个
    @score.setter装饰器作为为score参数赋值的装饰器，可以像访问类的属性一样访问方法。
    @classmethod 用在类定义中修饰一个方法函数，作用是，后续不管是从类中还是实例中调用该方法，这个方法
    将类本身作为self这个参数指向的对象，而不是指向实例；
    @staticmethod 在类中定义的函数正常情况下是作为类的一个方法，@staticmethod可以使该函数仍然是1个独立
    的函数，只是因为这个类要用到这个函数的结果(如环境变量设置或根据判断结果进行后续操作)，为了方便代码
    维护管理而将这个函数放在了这个类中。

13. 数据库表中生成随机id方法： def next_id():  =>  return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

14. 正则表达式的贪婪模式与非贪婪模式：如pattern1=re.compile(r"\w+")=>贪婪,pattern2=re.compile(r"\w+?")=>非贪婪，
    result1=re.match(pattern1,"aaabc") 匹配结果是"aaabc"，用pattern2匹配结果是"a"；
    re.match从头开始匹配字符串，如果pattern是一个确定的字符串，如pattern=re.compile(r"hello")，则
    result=re.match(pattern,"hellooo world!")匹配结果是"hello"，匹配字符串成功后匹配终止，不再继续向后匹配，匹配
    结果是一个SRE_Match对象，使用result.group()方法获取匹配后的字符串。
    re.search()与re.match()用法几乎一样，区别在于，search()扫描整个string查找匹配，找到匹配字符串就跟match()一样
    返回，不继续向后匹配。
    
15. 使用re.findall匹配字符串时候，要注意被匹配的对象是str对象，html中换行在str对象中以\n字符的形式存在，匹配时flags
    参数要为re.S，且写正则表达式时候要注意换行符的匹配！！！否则可能出现匹配后不报错也不停止匹配光标不停闪动的情况；

16. python3下打印汉字报错：
    (1)UnicodeEncodeError: 'gbk' codec can't encode character '\ufffd' in position 0: illegal multibyte sequence
    原因是dos控制台是用gbk编码，而抓取response后，使用了response.encoding="utf-8"编码，应该将响应内容编码为gbk
     ==> response.encoding="gbk"即可解决整个整个问题；
    (2)UnicodeEncodeError: 'gbk' codec can't encode character '\xa0' in position 21: illegal multibyte sequence，
    这个错误可以使用xx.encode("gbk","ignore").decode("gbk","ignore")
    或者xx.encode("gbk","replace").decode("gbk","replace")；

17. 爬取ajax动态加载页面
    参考：https://zhuanlan.zhihu.com/p/24982283
    判断是否是动态加载：直接爬取目标页面，使用BeautifulSoup处理后print到桌面(bs处理后更容易阅读)，与浏览器中打开的
    目标页面进行比对，print内容有缺失，则是ajax动态加载；
    解决方法：
    (1)chrome浏览器按F12，Network标签下看XHR或Doc，点击后显示print中没有的信息，则缺失的内容是通过整个url
    传送进来的，找这个url的规律，构造url继续爬；
    (2)使用神器selenium+phantomjs，缺点是，phantomjs比较慢，一般需要开多线程；
    注意问题：使用隐式等待加载页面，在locator使用时注意，比如使用 ...located((By.CLASS_NAME,"mm-p-cell-right"))，
    用于定位的元素中间不能有空格，不能使用  ...located((By.CLASS_NAME,"mm-p-info-cell clearfix")) 这种；

18. 杂项：
    (1)pip安装的库文件，可以用pip uninstall xx 卸载；
    (2)python3下打开网页， import webbrowser ==> webbrowser.open(url地址)；

19. 连接mongodb数据库：mongod --dbpath d:\mongodb\DB\data --logpath d:\mongodb\DB\logs --fork，注意，需要先建立
    data、logs再进行连接，--fork表示后台运行；
    mongo shell要使用，需要先使用mongod运行服务，再使用命令mongo直接打开mongo shell

20. dict对象取出数据，可以使用aa.get('bb')的方式，取出aa这个dict中key名为bb的value，也可以使用aa['bb']的形式取出；

21. 技巧：
    (1)content = dict(xx)
       with open('result.txt','a',encoding='utf-8') as f:
           f.write(json.dumps(content,ensure_ascii=False)+'\n')
           f.close()
    向文件中写入dict对象时，因为写入文件只能是str对象，所以需要使用json将content序列化成str对象，目前写入
    result.txt中的是unicode字符串，使用ensure_ascii=False配合encoding='utf-8'，将写入result.txt的结果变成utf-8编码；
    (2)使用selenium驱动浏览器，浏览器驱动程序所在路径中不能有汉字，否则会爆geckodriver在环境变量PATH中找不到的错误；

21. python3下的字符使用unicode编码，ord()函数获取字符对应的ascii编码,chr(x)获取数字x对应的ascii字符；
    hex()函数将一个整数转换成16进制字符串；
    s="人生苦短"中，s是个字符串，它本身存储的是字节码，直接在解释器交互界面下写代码，字节码的格式决定于当前解释器的
    编码格式，如对于windows的cmd就是gbk，如果是先保存再执行，在执行时根据保存时的编码格式将代码载入解释器；
    打印str对象，实际就是将字节流发送到shell，如果字节流的编码格式与shell编码格式不同，就会出现乱码；打印unicode
    对象，系统自动将其转换为shell的编码格式，不会出现乱码；
    reload(sys) => sys.setdefaultencoding('utf-8')
    总结：str对象是字节码，python3下读入内存的str都是使用unicode编码表示(01表示的数据)，优点是能够跨平台使用，
    unicode对象使用encode()方法编码为特定编码字节流数据bytes对象(貌如b'\xe4\xb8\xad\xe6\x96\x87'，这是16进制表示的
    二进制数据)，使用decode方法解码为str ； str对象是字节码，bytes对象是字节流；
    格式化问题:print('%2d-%02d' % (3,3))，其中%2d表示这个占位符是个两位数，不足两位数开头用空格填充，%02d表示这个
    占位符是2位数，不足两位数开头用0填充；

22. list是有序对象，dict是无序的；
    if x 的含义是，只要x是非零数值、非空字符串、非空list，就判断为true，否则为false；
    判断dict中是否存在某个key：使用 'xx' in d 判断时，存在返回true，否则返回false；使用d.get('xx',-1)判断时，存在
    就返回key为'xx'的value，不存在则返回指定的值 -1；
    可以用max()函数取list中的最大值；

23. 位置参数，默认参数，可变参数(形式为*args，可以直接传入任意多个数字，也可以*L的形式传入一个list/tuple)，
    关键字参数(**kw，可以key-value的形式传入任意多个键值对，也可以**dict的形式传入一个dict)，
    命名关键字参数(形式为(a,b,*,place,time),a、b是必选参数，额外的关键字参数只能是place、time，可以没有；当参数中
    存在可变参数*args时，其后跟随的命名关键字参数不用再前置一个*，命名关键字参数place、time可以设置缺省值，
    如place='Beijing')，
    dict迭代：迭代key的形式for key in d，迭代value的形式for value in d.values()，同时迭代key和value的形式
    for k,v in d.items() ;
    isinstance(x,(int,float))，判断x是否是int或float中的一种类型；
    生成器--generator是一种一边循环一边计算的机制；
    生成器有两种形式，圆括号的列表生成式和带有yield语句的generator function；
    迭代器：可以使用next()函数调用并不断返回下一个值的对象称为迭代器，生成器都是迭代器，list/tuple、dict/set、str
    是可迭代对象iterable，但不是迭代器，使用iter()方法可以使其编程迭代器；

23. map(f,[1,2,3]),将函数f()作用在list的每个值上，生成一个新的iterator；
    reduce(f,[1,2,3])，f()函数必须接收2个参数，并且将函数结果作为新的参数与后续的一个值继续传入f()进行计算；
    filter(f,[1,2,3])，将f()函数作用在list的每个值上，根据结果是True/False，决定保留或丢弃该元素，返回的是1个Iterator；
    sorted([1,-2,-13,9,53,-35],key=abs)，使用key参数传入自定义函数实现自定义排序，key函数先作用于list中的每个元素，
    再根据得到的结果进行排序，最后显示为原字符，反向排序时，设置reverse=True即可；

24. 'just to test it'.upper()，将所有字母转换成大写；
    'JUST TO TEST IT'.lower(),将所有字母转换成小写；
    'JUST TO TEST IT'.capitalize()，将字符串的首字母转换成大写，其余转换成小写；
    'JUST TO TEST IT'.title(),将字符串中所有单词的首字母转换成大写，其余转换成小写；
    判断字符串大小写函数  .isupper  .islower  .istitle

25. 使用闭包结构时，返回函数中不能引用循环变量，如下：
    def count():
        fs = []
        for i in range(1,4):
            def f():
                return i*i
            fs.append(f)      #此处，将函数f直接添加进了列表fs，相当于把i*i加进了fs，此时没有计算结果，而是引用了
        return fs             #循环变量i，当循环结束时，i=3，当调用count()函数，返回结果是fs=[i*i,i*i,i*i]，此时并没有
                              #计算结果，使用f1,f2,f3=count()调用函数，得到结果是f1=i*i,f2=i*i,f3=i*i,执行f1()/f2()/f3()，
                              #此时计算i*i的值，而此时的i=3，所已f1()=f2()=f3()=9；
                              ##改成fs.append(f())，不是将带有循环变量的函数加入而是直接将结果写入，即可正确运行；
    闭包结构的函数,如函数f(*args)返回的是函数sum，使用方法，首先sum=f(*args)拿到返回函数sum，之后sum()执行sum函数，当
    f(*args)返回sum时，相关参数和变量都保存在返回函数中；

26. 装饰器的本质其实就是一个闭包，只不过是以一个函数作为传入参数，返回的是一个函数wrapper，wrapper函数先打印日志，之后
    调用传入的函数；
    ```
    def log(func):
        @functools.wraps(func)   #当使用@语法@log装饰now函数相当于执行now=log(now)，返回一个函数，原来的now()函数仍然
        def wrapper(*args,**kw): #存在，此时now变量指向了新的函数wrapper，now的__name__属性也变成wrapper，
            print('call %s():' % func.__name__)   #@functools.wraps(func)作用是@log装饰后now函数的__name__属性值仍是now；
            return func(*args,**kw)
        return wrapper
    ```
27. Python网络编程，就是在Python程序本身这个进程内，连接别的服务器进程的通信端口进行通信；
    xx.split(' ',1)表示以空格作为分隔符，只分隔1次；
    if x:  这个判断语句是说，当x是None、0、False则条件成立，if not x:  与之相反；
    定义类的时候，类中定义的方法的第一个参数self默认指向实例，详见笔记@classmethod与@staticmethod；

28. MongoDB使用中注意的点：
    (1)db.users.find(),在当前数据库下名为users的集合中查找所有文档，如果集合名称中包含空格、连字符"-"或者以数字开始，
    可以用代替语法来指代集合：db["3users"].find() 或者 db.getCollection("3users").find()；
    使用find方法，查询条件必须包含在大括号"{}"内，查询操作符必须包含在一个大括号内；
    db.users.find({badges:"black"}),这条语句既可以查找出 包含badges字段且其值是"black"  的文档，也可以是 包含一个
    名为badges的数组且这个数组中存在一个"black"元素(这个数组中也可以存在其他元素)  的文档；
    db.users.find({finished:{$gt:15,$lt:20}}),既可以表示查找 包含一个finished字段且其值大于15小于20 的文档，也可以
    表示查找 包含一个名为finished的数组且这个数组中至少有一个元素的值大于15小于20  的文档，如果要特别指明要查询的
    是数组，可以用db.users.find({"finished.0":{$gt:15,$lt20}})(dot natation方法)(这里的字段"finished.0"必须带双引号)或者
    db.users.find({finished:{{$elemMatch:{$gt:15,$lt20}}}})的方法；
    db.users.find({finished:[13,17,19,23]}),精确匹配，查找名为finished的数组且这个数组中元素的顺序和值是13，17，19，23的
    数组；
    (2)嵌入文档的查询：
    db.users.find({favorites:{artist:"Picasso",food:"pizza"}})，在当前数据库下的users集合中，查找 只包含artist、food字段
    并且符合条件artist="Picasso"、food="pizza"的名为favorites的嵌入文档；
    db.users.find({"favorites.artist":"Picasso"})，在当前数据库的users集合中，查找 包含一个名为favorites的嵌入文档
    且其artist字段是"Picasso" 的所有文档；
    (3)更新
    db.users.update({finished:{$gt:15,$20}},{$set:{finished:[1,2,3]}},{multi:"true"}{upsert:"true"}),第一个参数是
    过滤条件，拿到要更新的文档，第二个参数是需要更新的这个文档的字段(带有$set字段是更新字段，不带则是用第二个参数
    作为文档更新整个文档；如果目标文档中不存在这个字段，就会新建这样一个字段)，
    第三个参数是指定更新找到的所有符合过滤条件的文档(可选参数，不带这个参数则只更新查找到的第一个文档)，第四个参数是
    可选参数，带有这个参数指明：在当前集合中查找不到符合过滤条件的文档，则新建这样一个文档,不带这个参数找不到符合
    过滤条件的文档则不做任何操作；
    第四个参数可用在scrapy的pipeline模块编写去重代码，将第二个参数设置为{$set:dict(item)}的格式；
    (4)删除
    db.users.remove({finished:19},{justOne:"true"})，删除 包含一个finished字段且这个字段的值是19 的文档，第二个
    参数是可选参数，不加第二个参数是指删除所有符合过滤条件的文档；

29. (1)xss(跨站脚本攻击)的本质是html页面对用户输入过滤不严，导致用户输入js脚本，当其他用户点击这个脚本，脚本执行，执行
    盗取用户信息、执行非法操作等；
    (2)csrf/xsrf(跨站请求伪造)原理是:用户正常登录某网站，在没有退出当前网站登录的前提下，又浏览另外一个网站(黑客构造的
    陷阱服务器，常见的比如在当前登录网站页面跳出"中奖"小弹框来诱使用户访问)，在这个陷阱服务器中，黑客诱使用户点击某个
    链接，而这个链接是黑客构造的"恶意请求访问"伪装成的，发送到用户之前登录且没有退出的网站，由于这个恶意请求是从用户
    本机浏览器发送，也就可以在请求头中加入cookie验证信息，结果就是目标服务器把陷阱站点发送的恶意请求当成了已登录
    正常用户发送的请求，结果就是黑客伪装成已经登录的真实用户向服务器发送请求并被服务器执行；
    要防御csrf，一个有效的措施用户第一次登录的时候，再返回的登陆框的html页面中带上一个服务器生成的 "_xsrf" 伪随机值字段，
    之后用户每一次向该服务器发送post请求都带上该字段，如果是陷阱站点发送的伪造请求，陷阱站点可以拿到浏览器的cookie(因为
    伪造请求也是从本机浏览器发出)，但是没有 "_xsrf" 字段，这个字段不像cookie那样存储在本机，而是包含在服务器返回的html
    代码中，没有之前的登录动作，陷阱站点也就没有这个字段，服务器就可以判定这是恶意构造的请求；

30. 模拟登录中验证码的处理方法：
    (1)借助第三方库实现自动识别，如
    (2)人工识别：在代码中提取验证码url，之后，有两种处理方法：
        ①在浏览器打开，之后在浏览器中输入验证码；
        ②构造一个单独函数，在代码中将验证码写入本地文件，查看，再通过一个input()语句读入验证码，返回结果；

31. jquery选择器返回的是一个list，当DOM中没有符合条件的节点，会返回一个空的list "[]"，；
    (1)$('#js-page'),查找id是js-page的节点；(一般DOM中的id是唯一的，方便拿到目标节点)
    (2)$('.js-page')，查找class属性值是js-page的所有节点；
    (3)$('[class=js-page]')，查找class属性值是js-page的所有节点，值中间有空格，需要双引号包含起来；
       所有属性都可以使用"[]"方式，做为查找条件，如[name=js-actiev] name属性值是js-actiev的所有节点；
       [class^=js-] 查找所有class属性值以"js-"开头的节点，[class$=js-]以"js-"结尾的节点；
    (4)组合查找，把查找条件堆叠在一起，中间没有空格，形如：div.red、div[name=js-color]；
    (5)多项选择器，用逗号"，"分隔开的两个查找条件并行查找，如$('p,div')把<p>和<div>节点都选出来；
    (6)层级选择器，$('ancestor  descendant')，层级之间用空格隔开，不要求是直属子节点，隔几层都可以，如$('ul.lang  li')
    (7)子选择器$('parent>child')，类似层级选择器，但是限定层级之间必须是直属关系；
    (8)过滤器(Filter)，如$('ul.land  li:first-child')， :first-child、:last-child、:nth-child(3)、
        :nth-child(even)序号为偶数的元素、:nth-child(odd)奇数；
    (9)表单相关，查廖雪峰js教程；

32. PyQuery()处理后得到的是一个pyquery.pyquery.PyQuery对象，是一个list，可以继续对该对象进行查找；
    对PyQuery()处理结果进行遍历，需要调用.items()方法(形如items=pq('li>a').items())，结果是一个generator，之后可以使用
    形如for item in items:  进行遍历，注意items没有括号； 
    如果html文档中没有查找到符合条件的节点，返回一个空的list(空list用if判断是false条件，如 if []: 这个判断结果是false)；
    .text()方法获取结果中所有的文本信息；
    .attr('xx')方法获取结果的属性信息；
    过滤器，根据节点在文档中出现的顺序精确定位某一节点,序号从零开始 :first :last :even :odd :eq :lt :gt ，如pqobj('li:eq(2)>a') ；
    表单相关 :checked :selected :file  ；
	
33. if..elif..else语句是当一个判断语句为true后就不再执行后续的判断；
    if..if..语句，可以看作是分别省略elif、else的两个独立的判断模块，不管第一个判断语句是否成立，第二个判断语句都会执行；
	
34. try..except as e:，使用这种结构运行程序时，如果出现错误，捕获错误的同时程序也就结束了，可以在except语句块中使用
    logging.exception(e)，抛出错误的同时程序继续向下执行；
	
35. 使用multiprocessing模块开启多进程，记录断点方法：
	(1)把被遍历对象中所有遍历过的条目记录到一个文件中，遇到中断，
	
36. 从list中删除元素，使用remove方法，如 L.remove('a');
	open方法错误处理使用errors参数，如 with open(r'xxxx','r',encoding='utf-8',errors='ignore')  ,errors参数值可以是ignore或者replace；

37. (1)使用BeautifulSoup中,bsobj.find('h3',text='tatta')表示选择文本内容是tatta的h3标签，可以继续使用.parrent定位标签，如果不写h3，查找
    结果是文本内容。   
    (2)break/continue方法只能用在被for..in或while包围的循环块中，不能在外围没有for..in或while的情况下用在if判断中,break是直接
	跳出当前loop,continue是跳过当前这次循环进入下一次循环；
	
38. 将mysql数据库中数据导入.txt文件中:
	mysql -uroot -proot -h192.168.1.109 czhd -e"select uid from tbl_person">d:\renren\renren.txt
	
39. mysql下建表命令:
    ```
    DROP TABLE IF EXISTS `wanfang_base`;
    CREATE TABLE `wanfang_base` (
      `id` int(128) auto_increment NOT NULL COMMENT 'SID',    ##id自增
      `title` varchar(255) DEFAULT NULL COMMENT '标题',
      `content` text COMMENT '内容',
      `name` varchar(255) DEFAULT NULL COMMENT '姓名',
      `subject` varchar(255) DEFAULT NULL COMMENT '专业',
      `degree` varchar(255) DEFAULT NULL COMMENT '学位',
      `schoolname` varchar(255) DEFAULT NULL COMMENT '学校名字',
      `teacher` varchar(255) DEFAULT NULL COMMENT '导师',
      `date` text COMMENT '毕业时间',
      `num` text COMMENT '分类号',
      `url` text COMMENT '网址',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ```
40. 查看list中某个元素的索引位置  L.index('xx') 
    list.remove('xx'),删除list中的指定元素，前提是这个元素在list中是存在的；
	
41. set的union、intersection、difference操作:
    a = set(list1)|set(list2),union操作，生成包含list1和list2的所有数据的新集合a；
	b = set(list1)&set(list2),intersection操作，生成包含list1和list2中共同元素的新集合；
	c = set(list1)-set(list2),difference操作，生成在list1中出现但不再list2中出现的元素的集合；
	
42. scrapy相关
    (1)如果提取到的url是相对路径，可以使用response.urljoin()，将相对路径转换成绝对路径的url；
	(2)scrapy crawl spidername -o xx.txt ,使用 -o 参数将爬取结果保存，根据文件名后缀自动判断保存文件的格式,可以是txt、json、jl、csv、xml等格式；
	(3)常用参数：
	    ①scrapy crawl spidername ,通过crawl参数执行爬虫；
		②scrapy check ,相当于运行一次爬虫，有错误就抛出；
		③scrapy fetch url地址 ，调用scrapy的downloader抓取页面,日志打印完跟着是抓取的html源码；scrapy fetch --nolog url地址,不打印
		日志，只输出html源码；--headers 参数可以拿到请求头信息；--no-redirect 禁止重定向；
		④scrapy view url地址, 请求目标url，将html源码下载下来保存成一个文件，再用浏览器打开，ajax请求内容下载不到；
		⑤scrapy shell url地址，请求目标url并打开交互界面；
		⑥scrapy parse url地址 -c parse_page ,调用spider.py中解析html的函数parse_page，返回解析结果，-c是--callback的缩写；
		⑦scrapy runspider spidernam.py ,执行爬虫，与crawl的区别是，runspider后接的爬虫名带 .py 后缀；
		⑧scrapy version ,查看scrapy版本；scrapy version -v 查看scrapy版本及其依赖库的版本；
		⑨scrapy bench ,测试爬虫速度，需在spiders文件夹下执行；
	(4).extract_first(default='') ,设置默认值，防止报错
	
43. dos下配合管道命令过滤字符串，netstat -na|findstr "3333" ，注意被查询的字符需要用双引号包起来；

44. 正则表达式中匹配中文字符:  [\u4e00-\u9fa5]，匹配双字节字符(包括汉字在内): [^\x00-\xff] ;

45. (1)清空dict的方法: d.clear();
    (2)可以通过L.append({x:y})的形式动态地构造dict,然后插入到L中;
	
46. 形如——&name;&#dddd;&#xhhhh;——的一串字符是 HTML、XML 等 SGML 类语言的转义序列（escape sequence）。
    它们不是「编码」。以 HTML 为例，这三种转义序列都称作 character reference：第一种是 character entity reference，
	后接预先定义的 entity 名称，而 entity 声明了自身指代的字符。后两种是 numeric character reference（NCR），
	数字取值为目标字符的 Unicode code point；以「&#」开头的后接十进制数字，以「&#x」开头的后接十六进制数字。
	解码方式：from HTMLParser import HTMLParser
			  print HTMLParser().unescape('&#20013;&#22269;')
			  
47. 连接redis时，默认是连接的0号数据库，通过 select 1 命令切换到1号数据库；

48. linux下安装pip工具，安装不上时可以尝试使用easy_install pip安装之；

49. 查看list中某元素的位置 list.index('xx')

50. selenium中使用xx.send_keys('xxx')报错 cannot focus element 解决方法:
    from selenium.webdriver.common.action_chains import ActionChains  
	action = ActionChains(driver)  
	action.move_to_element(e1).click().send_keys("xhsintcdw760").perform()  
	用上述方式传递值给元素节点;
    
51. selenium webdriver带正常的浏览器扩展插件等设置启动chrome方法:
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir="+r"C:\Users\muyal\AppData\Local\Google\Chrome\User Data")  #google路径需要查看
    browser = webdriver.Chrome(chrome_options=options)
	
52. (1)BeautifulSoup中使用text匹配html标签时,可以使用正则表达式,bsobj.find('a',text=re.compile(r'匹配(\d+)个字符串'));
    (2)使用next_sibling获取下个节点时,要注意:
	<td>text1</td>
	<td>text2</td>
	这种情况下,使用bsobj.find('td',text='text1').next_sibling抓取到的是两个<td>标签之间的 \n 换行符,如果要拿到text2所在节点,需要使用两次next_sibling
	bsobj.find('td',text='text1').next_sibling.next_sibling

53. requests中使用socks5代理,需要安装pysocks模块,pip install pysocks,安装即可,用时不需要导入,代理格式如下:
    http/https代理:{'http':'1.1.1.1:8880'}/{'https':'1.1.1.1:8880'}
	socks5代理:{'http':'socks5://user:passwd@host:port'}/{'https':'socks5://user:passwd@host:port'}
    
54. tesseract 4.0版本需要搭配 java 8 版本,高版本java环境会报错。 
    
55. python下使用','.join(list)将list中数据写到mysql对应字段下报错: TypeError: sequence item 0: expected string, int found
    处理方法: 
	(1)','.join(str(item) for item in list)
	(2)','.join(map(str,list))

56. 直接使用json.loads()反序列化data报错的情况，可以先json.dumps(data),然后通过json.loads(json.dumps(data))，完成反序列化；

57.windows下mysql的字段名中如果有小横杠'-'，使用时，需要使用 `` 将字段名包起来；


