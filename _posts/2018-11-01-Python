---
layout: default
authoer: muyalei
date: 2018-11-01
title: Python Socket 网络编程
tags:
   - python笔记
---


# Python Socket 网络编程
Socket 是进程间通信的一种方式，它与其他进程间通信的一个主要不同是：它能实现不同主机间的进程间通信，我们网络上各种各样的服务大多都是基于 Socket 来完成通信的，例如我们每天浏览网页、QQ 聊天、收发 email 等等。要解决网络上两台主机之间的进程通信问题，首先要唯一标识该进程，在 TCP/IP 网络协议中，就是通过 (IP地址，协议，端口号) 三元组来标识进程的，解决了进程标识问题，就有了通信的基础了。

本文主要介绍使用 Python 进行 TCP Socket 网络编程，假设你已经具有初步的网络知识及 Python 基本语法知识。

TCP 是一种面向连接的传输层协议，TCP Socket 是基于一种 Client-Server 的编程模型，服务端监听客户端的连接请求，一旦建立连接即可以进行传输数据。那么对 TCP Socket 编程的介绍也分为客户端和服务端：

## 客户端编程
### 创建 socket
首先要创建 socket，用 Python 中 socket 模块的函数 socket 就可以完成：
```
#Socket client example in python
 
import socket   #for sockets
 
#create an AF_INET, STREAM socket (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
print 'Socket Created'
```

函数 socket.socket 创建一个 socket，返回该 socket 的描述符，将在后面相关函数中使用。该函数带有两个参数：

- Address Family：可以选择 AF_INET（用于 Internet 进程间通信） 或者 AF_UNIX（用于同一台机器进程间通信）
- Type：套接字类型，可以是 SOCKET_STREAM（流式套接字，主要用于 TCP 协议）或者SOCKET_DGRAM（数据报套接字，主要用于 UDP 协议）
注：由于本文主要概述一下 Python Socket 编程的过程，因此不会对相关函数参数、返回值进行详细介绍，需要了解的可以查看相关手册

#### 错误处理

如果创建 socket 函数失败，会抛出一个 socket.error 的异常，需要捕获：
```
#handling errors in python socket programs
 
import socket   #for sockets
import sys  #for exit
 
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
```
那么到目前为止已成功创建了 socket，接下来我们将用这个 socket 来连接某个服务器，就连 www.google.com 吧。

### 连接服务器
本文开始也提到了，socket 使用 (IP地址，协议，端口号) 来标识一个进程，那么我们要想和服务器进行通信，就需要知道它的 IP地址以及端口号。

#### 获得远程主机的 IP 地址

Python 提供了一个简单的函数 socket.gethostbyname 来获得远程主机的 IP 地址：
```
host = 'www.google.com'
port = 80
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
```
现在我们知道了服务器的 IP 地址，就可以使用连接函数 connect 连接到该 IP 的某个特定的端口上了，下面例子连接到 80 端口上（是 HTTP 服务的默认端口）：
```
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
```
运行该程序：
```
$ python client.py
Socket created
Ip of remote host www.google.com is 173.194.38.145
Socket Connected to www.google.com on ip 173.194.38.145
```

### 发送数据
上面说明连接到 www.google.com 已经成功了，接下面我们可以向服务器发送一些数据，例如发送字符串GET / HTTP/1.1\r\n\r\n，这是一个 HTTP 请求网页内容的命令。
```
#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    #Set the whole string
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'
```
发送完数据之后，客户端还需要接受服务器的响应。

接收数据
函数 recv 可以用来接收 socket 的数据：
```
#Now receive data
reply = s.recv(4096)
 
print reply
```
一起运行的结果如下：
```
Socket created
Ip of remote host www.google.com is 173.194.38.145
Socket Connected to www.google.com on ip 173.194.38.145
Message send successfully
HTTP/1.1 302 Found
Cache-Control: private
Content-Type: text/html; charset=UTF-8
Location: http://www.google.com.sg/?gfe_rd=cr&ei=PlqJVLCREovW8gfF0oG4CQ
Content-Length: 262
Date: Thu, 11 Dec 2014 08:47:58 GMT
Server: GFE/2.0
Alternate-Protocol: 80:quic,p=0.02

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Moved</TITLE></HEAD><BODY>
<H1>302 Moved</H1>
The document has moved
<A HREF="http://www.google.com.sg/?gfe_rd=cr&ei=PlqJVLCREovW8gfF0oG4CQ">here</A>.
</BODY></HTML>
```

### 关闭 socket
当我们不想再次请求服务器数据时，可以将该 socket 关闭，结束这次通信：

`s.close()`

### 小结
上面我们学到了如何：

1.创建 socket
2.连接到远程服务器
3.发送数据
4.接收数据
5.关闭 socket
当我们打开 www.google.com 时，浏览器所做的就是这些，知道这些是非常有意义的。在 socket 中具有这种行为特征的被称为CLIENT，客户端主要是连接远程系统获取数据。

socket 中另一种行为称为SERVER，服务器使用 socket 来接收连接以及提供数据，和客户端正好相反。所以 www.google.com 是服务器，你的浏览器是客户端，或者更准确地说，www.google.com 是 HTTP 服务器，你的浏览器是 HTTP 客户端。

那么上面介绍了客户端的编程，现在轮到服务器端如果使用 socket 了。





