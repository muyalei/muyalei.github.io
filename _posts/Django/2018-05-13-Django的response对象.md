---
layout: default
author: muyalei
date: 2018-05-13
title: Django的response对象
tags:
   - Django
---

***整理自[https://www.cnblogs.com/scolia/p/5635546.html](https://www.cnblogs.com/scolia/p/5635546.html)***

    回顾 HTTP 协议的通信核心，无非就是请求报文和响应报文之间的交互。而请求报文由客户端生成，也就是用户的浏览器；响应报文则由服务器生成，作为web应用的开发者，大多数工作就是构造一个合适的响应报文。在 django 中，请求报文已经被封装成了 HttpRequest 对象，该对象的创建是自动的，且会传递给视图函数作为第一个参数。而 HttpResponse 对象则需要 web 开发者自己创建，一般在视图函数中 return 回去。下面我们就来看看 HttpResponse 对象的各种细节。

    首先，这个对象由 HttpResponse 类创建，这个类位于 django.http 模块中，所以在使用的时候还先从模块中导入这个类。

例如：
```
from django.http import HttpResponse
```
　　然后，我们需要知道传递什么参数，这个时候先看看其构造函数是怎么样的。
```
HttpResponse.__init__(content='', content_type=None, status=200, reason=None, charset=None) 
```
　　content：可以是一个迭代器或字符串。如果是一个迭代器，HttpResponse 将立即处理这个迭代器, 把它的内容转成字符串，并丢弃这个迭代器。如果你需要从迭代器到客户端的数据响应以数据流的形式, 你必须用 StreamingHttpResponse 类代替；如果是一个字符串（迭代器处理后的或手动传入的），那么这个字符串将作为相应报文的主体内容，也就是说如果是一个 http 文档，那么这个文档将会放入响应报文的主体中，最后在浏览器中显示，这也是最为常用的方式之一。

　　content_type：用于指定 MIME 类型和编码，例如：“text/html; charset=utf-8”。客户端需要知道主体是什么类型的资源，才能调用相应的插件或内置的程序去处理。如果不传入，也就是为 None 时，将使用 DEFAULT_CONTENT_TYPE 的值来指定 MIME 类型，这个值默认为：'text/html';使用 DEFAULT_CHARSET 的值来指定文件编码，默认为：'utf-8'。

　　status：响应状态码，200代表成功，一般不需要改变，除非有特殊要求。

　　reason：原因短语，也就是 200 ok 中的 ‘ok’，因为客户端是根据状态码来判断响应是否成功的，所以 reason 的影响几乎为 0 ，只是对人的提醒而已。如果没有指定, 则使用默认响应短语。也就是 200 就对应于 ok，404 就对应于 not found。

　　charset：在response中被编码的字符集。如果没有给定（也就是为None），将会从 content_type 中提取，如果提取不成功， 那么 DEFAULT_CHARSET 的设定将被使用。
 
同样的，我们可以使用相关的属性去查看这些值：


`HttpResponse.content` ：表示内容的字符串，对应于我们传入的 content 参数的值。

`HttpResponse.charset` ：一个表示编码的字符串，对应于 charset 参数，如果实例化的时候没有给定，将从 content_type 中解析出来，如果解析失败，将使用 DEFAULT_CHARSET 的值。

`HttpResponse.status_code` :表示响应的状态码。在 1.9 中除非 reason_phrase 属性被显式的设置，否则在构造函数外修改状态码时，也会修改 reason_phrase 属性。也就是说，当我们在创建实例的时候，并没有设置 reason ，原来的状态码是 200 ，当我们在构造器外修改这个属性的时候，如修改成 404，那么 reason_phrase 属性就变成对应的 not found。

`HttpResponse.reason_phrase` ：表示响应的原因短语，对应于 reason 参数。在1.9中 reason_phrase 不再默认为全部大写字母。现在使用 HTTP 标准的默认原因短语。除非显式设置，reason_phrase 由status_code 的值的确定。

`HttpResponse.streaming` ：这个选项总是 False。由于这个属性的存在，使得中间件（middleware）能够区别对待流式 response 和常规 response 。

`HttpResponse.closed` ：如果响应已关闭，则是 True 的。

`HttpResponse.__setitem__(header, value)` :由给定的首部名称和值设定相应的报文首部。 header 和 value 都应该是字符串类型。

`HttpResponse.__delitem__(header)`:根据给定的首部名称来删除报文中的首部。如果对应的首部不存在将沉默地（不引发异常）失败。不区分大小写。

`HttpResponse.__getitem__(header)`: 根据首部名称返回其值。不区分大小写。

`HttpResponse.has_header(header)`: 通过检查首部中是否有给定的首部名称（不区分大小写），来返回 True 或 False 。

`HttpResponse.setdefault(header, value)`: 设置一个首部，除非该首部 header 已经存在了。

 另外，我们还可以使用类字典的方法来设置首部，例如：
```
>>> response = HttpResponse()
>>> response['Age'] = 120
>>> del response['Age']
```

注意：当调用 del 去删除的首部不存在时，会引发 KeyError 异常。 

　　但是，当我们设定 Cache-Control 首部和 Vary 首部时，推荐使用 patch_cache_control() 和 patch_vary_headers()方法，可以从 django.utils.cache 中导入它们。因为这两个首部通常有多个值，这些值都要逗号隔开。"patch" 方法可以确保这些值，例如由中间件添加的值不会被改变。而字典形式添加的，同名键的不同值会发生冲突，只有最后一个值有效。

　　另外，虽然标准的 HTTP 报文中要求首部的每一行都要使用换行符隔开，但是 django 已经帮我们做了这些，所以我们不用重复的添加换行符了，否则会触发 BadHeaderError 异常。

`HttpResponse.set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)` 

　　设置一个Cookie。参数与Python 标准库中的 Morsel Cookie 对象相同。

　　key：键名，字符串形式。

　　value：对应的值，字符串形式。

　　max_age：cookie 过期的相对时间，单位是秒。如果为None，则当浏览器关闭的时候过期。如果设置了 max_age 而没有设置 expires，则 expires 将根据 max_age 的值计算出来。

　　expires：设置 cookie 过期的绝对时间。应该是一个 UTC "Wdy, DD-Mon-YY HH:MM:SS GMT" 格式的字符串，或者一个 datetime.datetime 对象。如果 expires 是一个datetime 对象，则 max_age 会通过计算得到。

　　path:一个字符串，表示客户端回送 cookie 的路径，如果为‘/’，则表示该域名下的所以路径都将回送 cookie，如果是‘/blog/’；则在访问‘/blog/abc’或者‘/blog/def’等，所有包含该前缀的路径时，客户端都会回送 cookie。

　　domain：cookie有效的域。例如，其值为‘.scolia.com’时，那么在访问 www.scolia.com 或者 test.scolia.com 之类的时，都会回送 cookie ，当然通常会和 path 配合在一起使用。根据 HTTP 协议的要求，这个值必要要两到三个句点，从而防止出现 ‘.com’、‘.edu’、‘va.us’等形式的域名。当域为高层域时，只要两个句点就可以了，而高层域包括：.com、.edu、.net、.org、.gov、.mil、.int、.biz、.info、.name、 .museum、.coop、.aero、和.pro。其他的域则需要至少三个。

　　secure：当其为 True 时，表示只要在 https 连接的情况下才会回送cookie

　　httponly：当其为 True 时，JavaScript 等就不能访问对应的cookie了。当然这个标记并不是cookie标准中的，但目前市面上常用的浏览器都支持。灵活使用可以提供数据的安全性。

注意:

　　RFC 2109 和RFC 6265 都声明客户端至少应该支持 4096 个字节的Cookie。对于许多浏览器，这也是最大的大小。如果视图存储大于 4096 个字节的 Cookie，Django 不会引发异常，但是浏览器将不能正确设置 Cookie。

`HttpResponse.set_signed_cookie(key, value, salt='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=True)` 

　　与 set_cookie() 类似，但是在设置之前将用密钥签名，也就是常说的加盐处理。通常与 HttpRequest.get_signed_cookie() 一起使用。你可以使用可选的 salt 参数来增加密钥强度，但需要记住在调用 HttpRequest.get_signed_cookie() 时，也要把使用的 salt 参数传入，用于解密。

`HttpResponse.delete_cookie(key, path='/', domain=None)` 

　　在cookie中删除指定的 key 及其对应的 value。如果 key 不存在则什么也不发生，也就是不会引发异常。

　　由于 Cookie 的工作方式，path 和 domain 应该与 set_cookie() 中使用的值相同 —— 否则 Cookie 不会删掉。

`HttpResponse.write(content)` 

　　将 content 写到报文的主体中，这使得 HttpResponse 的实例类似于文件对象。

　　类似的还有：

　　`HttpResponse.flush()` ：将缓存区的内容写入到报文中

　　`HttpResponse.tell()` ：移动文件中的操作指针

 `HttpResponse.getvalue()`: 从 HttpResponse.content 中返回其值。这使 HttpResponse 的实例类似于数据流对象。

`HttpResponse.writable()`:总是 True，表示其是可写的。这使 HttpResponse 的实例类似于数据流对象。

 

`HttpResponse.writelines(lines)`:在内容中写入一行。不添加行分隔符。这使 HttpResponse 的实例类似于数据流对象。

* * * * * *

### HttpResponse的子类
Django包含了一系列的HttpResponse衍生类（子类），用来处理不同类型的HTTP 响应（response）。与 HttpResponse 相同, 这些衍生类（子类）存在于 django.http 之中。

`class HttpResponseRedirect` 

　　构造函数的第一个参数是必要的 — 用来重定向的地址。这些能够是完全特定的URL地址（比如，'http://www.yahoo.com/search/'），或者是一个不包含域名的绝对路径地址（例如， '/search/'）。关于构造函数的其他参数，可以参见 HttpResponse。注意！这个响应会返回一个302的HTTP状态码。

　　url:一个只读属性，表示代表响应将会重定向的URL地址（相当于Location 首部信息）。

`class HttpResponsePermanentRedirect` 

　　与 HttpResponseRedirect 一样，但是它会返回一个永久的重定向（HTTP状态码301）而不是一个“found”重定向（状态码302）。

`class HttpResponseNotModified` 

　　构造函数不会有任何的参数，并且不应该向这个响应（response）中加入内容（content）。使用这个意味着资源在用户最后一次请求之后，没有修改过（状态码304）。

`class HttpResponseBadRequest` 

　　与HttpResponse的行为类似，但是使用了一个400的状态码。表示一个错误的请求。

`class HttpResponseNotFound` 

　　与HttpResponse的行为类似，但是使用了一个404的状态码。表示资源没有找到。

`class HttpResponseForbidden` 

　　与HttpResponse的行为类似，但是使用了一个403的状态码。表示用户无权访问。

`class HttpResponseNotAllowed` 

　　与HttpResponse的行为类似，但是使用了一个405的状态码。表示请求的方法不被允许。 构造函数的第一个参数是必须的：一个允许使用的方法构成的列表（例如，['GET', 'POST']）。也就是说不在列表中的方法就是不被运行的方法。

`class HttpResponseGone` 

　　与HttpResponse的行为类似，但是使用了一个410的状态码。表示服务器曾经拥有过此资源。主要是在 web 站点进行维护的时候，通知客户端。

`class HttpResponseServerError` 

　　与HttpResponse的行为类似，但是使用了一个500的状态码。表示服务器内部错误。

*注意*：如果一个自定义的 HttpResponse 的子类实现了 render 方法，那么 django 会将其当作一个 SimpleTemplateResponse。 render 方法必须返回一个有效的响应对象。

* * * * * *

### JsonResponse
　　json是目前常用的一种数据格式，有时候我们需要返回一个json格式的数据，而 JsonResponse 提供了一个快捷的方法。

　　它是 HttpResponse 的一个子类，用来帮助用户创建JSON 编码的响应。它从父类继承大部分行为，下面看起构造函数：

`class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)`  

　　data:应该传递一个标准的 python 字典给它，它将其转换成 json 格式的数据。

　　encoder：默认为 django.core.serializers.json.DjangoJSONEncoder，用于序列化data。关于这个序列化的更多信息参见JSON 序列化。

　　safe ： 默认为True。如果设置为False，可以传递任何对象进行序列化（否则，只允许dict 实例）。如果safe 为True，而第一个参数传递的不是dict 对象，将抛出一个TypeError。

另外：它的默认 Content-Type 头部设置为application/json。

　　json_dumps_params：在1.9版本中新增，可以传递一个python标准的 json 库中，json.dump() 方法处理后的对象给它，用于生成一个响应。

#### 用法：
典型的用法如下：
```
>>> from django.http import JsonResponse
>>> response = JsonResponse({'foo': 'bar'})
>>> response.content
'{"foo": "bar"}'
``` 

#### 序列化非字典对象：
若要序列化非dict 对象，你必须设置safe 参数为False：
```
>>> response = JsonResponse([1, 2, 3], safe=False)
```

如果不传递safe=False，将抛出一个TypeError。

注意：

在EcmaScript 第5版之前，这可能会使JavaScript Array 构造函数崩溃。出于这个原因，Django 默认不允许传递非字典对象给JsonResponse 构造函数。然而，现代的大部分浏览器都已经实现EcmaScript 5，它删除了这种攻击性的数组。所以可以不用关注这个安全预防措施。

#### 修改默认的JSON 编码器：
如果你需要使用不同的JSON 编码器类，你可以传递encoder 参数给构造函数：
```
>>> response = JsonResponse(data, encoder=MyJSONEncoder)
```

* * * * * *

### StreamingHttpResponse 
`class StreamingHttpResponse` 

　　StreamingHttpResponse类被用来从Django流式化一个响应（response）到浏览器。当生产的响应太长或者占用太多的内存的时候，你可能会使用到它。例如，它对于生成大型CSV文件非常有用。

 

性能方面的考虑：

　　django是为了短链接而设计的，也就是说每次响应完毕之后都会断开连接。流式响应将会为整个响应期协同工作进程。这可能导致性能变差。

　　总的来说，你需要将代价高的任务移除 请求—响应 的循环，而不是求助于流式响应。

StreamingHttpResponse 不是 HttpResponse 的衍生类（子类），因为它实现了完全不同的应用程序接口（API）。尽管如此，除了以下的几个明显不同的地方，其他几乎完全相同：

- 应该提供一个迭代器给它，这个迭代器生成出字符串将用来构成内容（content）
- 你不能直接访问它的内容（content），除非迭代响应对象本身。这只在响应被返回到客户端的时候发生。
- 它没有 content 属性。取而代之的是，它有一个 streaming_content 属性。
- 你不能使用类似文件对象的tell()或者 write() 方法。那么做会抛出一个异常
StreamingHttpResponse 应该只在下面的情况下使用：请求是独立的，并且整个内容是不能重复的，在发生给客户端之前。因为其内容（content）是不能访问的，所以很多中间件是无法正常工作的。例如：ETag 和 Content- Length 首部就不能在流式相应中生成。

属性：

`StreamingHttpResponse.streaming_content` 

　　一个迭代器，包含内容字符串。

`StreamingHttpResponse.status_code` 

　　响应的状态码

`StreamingHttpResponse.reason_phrase` 

　　响应的原因短语

`StreamingHttpResponse.streaming` 

　　总是True，表示其是一个流式响应。

* * * * * * 

### FileResponse 

`class FileResponse` 

　　FileResponse是StreamingHttpResponse的衍生类（子类），为二进制文件做了优化。如果 wsgi server 来提供，则使用了wsgi.file_wrapper ，否则将会流式化一个文件为一些小块。

FileResponse 需要通过二进制模式打开文件，如下:
```
>>> from django.http import FileResponse
>>> response = FileResponse(open('myfile.png', 'rb'))
```
