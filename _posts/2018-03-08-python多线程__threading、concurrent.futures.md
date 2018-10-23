---
layout:     post
title:      python中的多线程__threading、concurrent.futures
subtitle:   
date:       2018-03-08
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - 多线程
    - python
---


### 全局解释器锁（GIL）
>Python 代码的执行是由Python 虚拟机（又名解释器主循环）进行控制的。Python 在
设计时是这样考虑的，在主循环中同时只能有一个控制线程在执行，就像单核CPU 系统
中的多进程一样。内存中可以有许多程序，但是在任意给定时刻只能有一个程序在运行。
同理，尽管Python 解释器中可以运行多个线程，但是在任意给定时刻只有一个线程会被
解释器执行。
对Python虚拟机的访问是由全局解释器锁（GIL）控制的。这个锁就是用来保证同时只
能有一个线程运行的。在多线程环境中，Python 虚拟机将按照下面所述的方式执行。
1.设置GIL。
2.切换进一个线程去运行。
3.执行下面操作之一。
 *指定数量的字节码指令。
 *线程主动让出控制权（可以调用time.sleep(0)来完成）。
4.把线程设置回睡眠状态（切换出线程）。
5.解锁GIL。
6.重复上述步骤。

"python中没有真正的多线程"，也就是上面这个原因。


### thread模块（python3中改名_thread）
>要避免使用thread模块，原因：<br>
避免使用thread 模块的另一个原因是它对于进程何时退出没有控制。当主线程结束
时，所有其他线程也都强制结束，不会发出警告或者进行适当的清理。如前所述，至少
threading 模块能确保重要的子线程在进程退出前结束。<br>
避免使用thread 模块的另一个原因是该模块不支持守护线程这个概念。当主线程退出
时，所有子线程都将终止，不管它们是否仍在工作。

### threading模块（推荐使用）
threading模块的Thread类是主要的执行对象，其重要属性：<br>
1.start()  #开始执行该线程
2.run()  #定义线程功能的方法（通常在子类中被应用开发者重写）
3.join(timeout=None)  #直至启动的线程终止之前一直挂起；除非给出了timeout（秒），否则会一直阻塞

### threading多线程并发实例
>通过*派生Thread的子类，并创建子类的实例*这种方式来进行一个并发实例：
（用到多线程时，可以这个为模板！）
```
#!/usr/bin/env python

import threading
import time
from atexit import register

loops = (4,2)

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        
       def run(self):
            
def loop(nloop,nsec):
    print('start loop',nloop,'at+',time.time())
    sleep(nsec)
    print('loop',nloop,'done at:%s', % time.time())
           
def _main():   #_main()函数同样是一个特殊函数，只有这个模块从命令行直接运行时才会执行该函数（并且不能被其他模块导入）。该函数会显示起止时间（让用户了解整个脚本运行了多久）
    print('starting at:',time.time())
    threads = []
    nloops = range(len(loops))
    
    for i in nloops:
        t = MyThread(loop,(i,loops[i]),loop.__name__)
        threads.append(t)
        
    for i in nloops:
        threads[i].start()
        
    for i in nloops:
        threads[i].join()

#atexit.register()是什么呢？这个函数（这里使用了装饰器的方式）会在Python 解释器中注册一个退出函数，也就是说，它会在脚本退出之前请求调用这个特殊函数。（ 如果不使用装饰器的方式， 也可以直接使用register(_atexit())）。
@register
def atexit():
    print('all DONE at:%s' % time.time)
    
if __name__=='__main__':
    main()
```

### 锁
>当多线程争夺锁时，允许第一个获得锁的线程进入临界区，并执行代码。所有之后到达
的线程将被阻塞，直到第一个线程执行结束，退出临界区，并释放锁。此时，其他等待的线
程可以获得锁并进入临界区。不过请记住，那些被阻塞的线程是没有顺序的（即不是先到先
执行），胜出线程的选择是不确定的，而且还会根据Python 实现的不同而有所区别。
#### 锁示例
1.不使用锁：（简单起见，没有使用派生Thread类的形式）<br>
```
from threading import Thread,currentThread
from time import sleep,ctime

class CleanOutpuSet(set):
    def __str__(self):
        return ','.join(x for x in self)
        
remaining = CleanOutputSet()

def loop(nsec):
    myname = currentThread().name
    remaining.add(myname)
    print('%s Started at:%s' % (ctime(),myname))
    sleep(nsec)
    remaining.remove(myname)
    print('%s Completed %s (%d secs)' % (ctime(),myname,nsec))
    print('(remaining:%s)' % (remaining or 'NONE'))
    
def main():
    for pause in range(5):
        Thread(target=loop,args=(pause,)).start()
```
期望的执行结果如下所示：
```
[Sat Apr 2 11:37:26 2011] Started Thread-1
[Sat Apr 2 11:37:26 2011] Started Thread-2
[Sat Apr 2 11:37:26 2011] Started Thread-3
[Sat Apr 2 11:37:29 2011] Completed Thread-2 (3 secs)
(remaining: Thread-3, Thread-1)
[Sat Apr 2 11:37:30 2011] Completed Thread-1 (4 secs)
(remaining: Thread-3)
[Sat Apr 2 11:37:30 2011] Completed Thread-3 (4 secs)
(remaining: NONE)
```
实际可能出现如下的执行结果：
```
[Sat Apr 2 11:37:56 2011] Started Thread-1
[Sat Apr 2 11:37:56 2011] Started Thread-2
[Sat Apr 2 11:37:56 2011] Started Thread-3
[Sat Apr 2 11:37:56 2011] Started Thread-4

>[Sat Apr 2 11:37:58 2011] Completed Thread-2 (2 secs)
[Sat Apr 2 11:37:58 2011] Completed Thread-4 (2 secs)
(remaining: Thread-3, Thread-1) 
(remaining: Thread-3, Thread-1)  

[Sat Apr 2 11:38:00 2011] Completed Thread-1 (4 secs)
(remaining: Thread-3)
[Sat Apr 2 11:38:00 2011] Completed Thread-3 (4 secs)
(remaining: NONE)
all DONE at: Sat Apr 2 11:38:00 2011
```
出现这种结果的原因：程序运行时，并发执行4个线程，碰到sleep()，当前线程阻塞，转而执行其他线程；sleep()结束，第一个进入临界区的
线程被执行，从remainning中删除自己对应的myname值，执行一小段时间后（本例执行到打印```>[Sat Apr 2 11:37:58 2011] Completed Thread-2 (2 secs)```），阻塞当前线程，
退出临界区，释放锁，所有线程竞争锁，Thread-4获得锁，进而执行，同样对这个变量==>remaining 操作，从remaining中删除自己对应的1个myname值，
达到执行时间，阻塞当前线程，退出临界区，释放锁，然后Thread-2、Thread-4又分别竞争到锁，执行打印命令，就看到了上面的结果。

>*I/O 和访问相同的数据结构都属于临界区，因此需要用锁来防止多个线程同时进入临界区。*<br>
个人理解：在被 Thread派生类 实例化的函数外的数据结构，是所有线程公用的，像例子中的remaining集合、打开的文件对对象等。

2.加锁，禁止多个线程修改同一个变量：<br>
示例代码：（简单起见，同样不使用类）
```
from threading import Thread,currentThread,Lock as lock  #引入锁Lock

def loop(nsec):
    myname = currentThread().name
    #Lock().acquire()
    with Lock():
        remaining.add(myname)
        print('%s Started %s' % (ctime(),myname))
    #Lock().release()
    sleep(nsec)
    #Lock().acquire()
    with Lock():
        remaining.remove(myname)
        print('%s Completed %s (%d secs)' % (ctime(),myname,nsec))
        print('(remaining:%s)' % (remaining or None))
    #Lock().release()    
```

### 线程间通信
线程之间使用使用queue(python2.X称为Queue)进行通信```from queue import Queue```，不能使用list等数据结构！
异常：<br>
*Empty  #当对空队列调用get*()方法时抛出异常
*Full  #当对已满的队列调用put*()方法时抛出异常
方法：<br>
*qsize()  #返回队列大小（由于返回时队列大小可能被其他线程修改，所以该值为近似值）
*empty()  #如果队列为空，则返回True；否则，返回False
*full()  #如果队列已满，则返回True；否则，返回False
*put(item,block=True,timeout=None)  #将 item 放入队列。如果block 为True（默认）且timeout 为None，则在有可用空间之前阻塞；如果timeout 为正值，则最多阻塞timeout 秒；如果block 为False，则抛出Empty 异常
*put_nowait(item)  #和put(item, False)相同
*get(block=True,timeout=None)  #从队列中取得元素。如果给定了block（非0），则一直阻塞到有可用的元素为止
*get_nowait()  #和 get(False)相同
*task_done()  #用于表示队列中的某个元素已执行完成，该方法会被下面的join()使用
*join()  #在队列中所有元素执行完毕并调用上面的task_done()信号之前，保持阻塞

### 线程的替代方案
1.multiprocessing 模块  #多进程，接口很类似threading
2.concurrent.futures 模块  #ThreadPoolExecutor执行多线程，ProcessPoolExecutor执行多进程，（都是异步？）


### 爬虫中使用多线程代码示例
1.不使用Queue队列的threading多线程爬虫
```
import os
from threading import Thread,currentThread,Lock
from queue import Queue
import re
import requests
import time
from bs4 import BeautifulSoup


class MyThread(Thread):
    def __init__(self,func,args,name=''):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(*self.args)


def get_data(city_code,city_name):
    base_url = 'http://m.51job.com/search/joblist.php?jobarea={city_code}&funtype=0405%2C0404&from=jobsearch_button&pageno={page_num}'

    for page_num in range(10000):
        url = base_url.format(city_code=city_code,page_num=page_num)
        response = requests.get(url)
        response.encoding = 'utf-8'
        bsobj = BeautifulSoup(response.text,'lxml')

        #判断是否翻页
        result = int(bsobj.find('p',{'class':'result'}).find('span').get_text()) #返回结果数目
        if result<=30: #返回结果<=30条，不存在下一页，解析完本页，直接跳出循环，继续查询下个城市
            items = bsobj.find('div',{'class':'items'}).findAll('a',href=True)
            for item in items:
                url_wap = item.attrs['href']
                url_pc = 'http://jobs\.51job.com/\.\*\?/{id}.html\?s=01&t=0'.format(id=item.attrs['href'].replace())
                f_wap.write(url_wap+'\t'+city_name+'\n')  #这里是否加个锁更好呢？
                f_pc.write(url_pc+'\t'+city_name+'\n')
                print(url_wap,url_pc)
            break
        else:
            if not bsobj.find('a',{'class':'next on'}): #存在下一页时，判断是否已经是最后一页
                #提取信息
                items = bsobj.find('div',{'class':'items'}).findAll('a',href=True)
                for item in items:
                    try:
                        url_wap = item.attrs['href']
                        url_pc = 'http://jobs\.51job.com/\.\*\?/{id}.html\?s=01&t=0'.format(id=re.search(r'http://m.51job.com/search/jobdetail.php\?jobid=(.*?)&jobtype=0',item.attrs['href']).group(1))
                        f_wap.write(url_wap+'\t'+city_name+'\n')  #这里是否加个锁更好呢？
                        f_pc.write(url_pc+'\t'+city_name+'\n')
                        print(url_wap,url_pc)
                    except Exception as e:
                        print('出错啦！！错误信息：%s' % str(e.args))
            else:
                break


def main():
    city_list = {'010000':'北京','020000':'上海','030200':'广州','040000':'深圳','090200':'成都','200200':'西安','120200':'济南','120300':'青岛','080200':'杭州','190200':'长沙','70400':'无锡','250200':'昆明'}
    threads = []

    for city_code,city_name in city_list.items():
        t = MyThread(get_data,(city_code,city_name))
        threads.append(t)

    for i in range(len(city_list)):
        threads[i].start()

    for i in range(len(city_list)):
        threads[i].join()

    print('all DONE at:%s' % time.ctime())


if __name__=='__main__':

    f_wap = open(os.getcwd()+r'\51job_wap.txt','a+',encoding='utf-8',errors='ignore')
    f_pc = open(os.getcwd()+r'\51job_pc.txt','a+',encoding='utf-8',errors='ignore')

    main()

    f_wap.close()
    f_pc.close()

```
2.使用concurrent.futures实现多线程
```
def get_data(params):
    city_code = params[0]
    city_name = params[1]
    base_url = 'http://m.51job.com/search/joblist.php?jobarea={city_code}&funtype=0405%2C0404&from=jobsearch_button&pageno={page_num}'

...............被执行函数与上面相同.......................

def main():
    city_list = {'010000':'北京','020000':'上海','030200':'广州','040000':'深圳','090200':'成都','200200':'西安','120200':'济南','120300':'青岛','080200':'杭州','190200':'长沙','70400':'无锡','250200':'昆明'}

    with ThreadPoolExecutor(32) as executor:
        for city_code,city_name in city_list.items():
            params = [city_code,city_name]
            executor.submit(get_data,params)  #这里注意，submit只接受 调用函数及其传入参数 这2个参数，如果需要向被调用的函数传入多个参数，
                                              #可以将所有参数写入一个list，将这个list作为参数传入被调用函数。
    print('all DONE at:%s' % time.ctime())

```


### 爬虫中使用
1.如果数据量不大，可以直接使用threading(可能用到queue)，开启多线程。<br>
在一个进程中启用多线程，效率会提高很多，但不是最高。<br>
2.如果数据量很大，可以使用multiprocessing模块中的进程池，开启异步，通过多进程+异步的形式，实现效率最大化。

