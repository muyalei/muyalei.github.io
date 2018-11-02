---
layout: default
author: muyalei 
date: 2017-09-13
title: python中使用tesseract
tags:
   - python笔记
---


转载自[https://www.polarxiong.com/archives/python-pytesser-tesseract.html](https://www.polarxiong.com/archives/python-pytesser-tesseract.html)

### PyTesser
PyTesser在Python Package Index中的版本仍为最初的2007年的0.0.1版，怀疑是不是已经不再维护。PyTesser似乎仅仅是在Tesseract的可执行程序tesseract.exe基础上写了一个面向Python的接口，就是通过shell执行tesseract命令获取返回值。

对于Tesseract这种C++编写的库采用可执行文件方式通过shell来建立库和Python的通信似乎无可厚非，但PyTesser在这里就犯了几个致命的错误：

- 直接集成tesseract.exe，导致x64不兼容，Linux不兼容等问题；
- Tesseract版本过老且不可手动替换文件升级，其Tesseract版本为2007年之前版本；
- PyTesser提供的接口代码效率不高（当时Tesseract支持度不高的原因）。

总的来说，除非PyTesser作出升级，否则PyTesser是基本没有价值的，不推荐使用。

### 关于Tesseract
Tesseract是一个流行的OCR（Optical Character Recognition，光学字符识别）库，通俗来说就是文本识别。Tesseract最初由HP（就是惠普啦）在1985年开始研发，后面貌似就没啥太重大的进展了；直到2005年HP将Tesseract开源，2006年开始交给Google维护。

Tesseract在进入3.0版本后各方面功能都有了长足的发展，尤其是3.02.02版本开始提供C-API，使得通过动态链接库与其他编程语言混合开发成为了可能。

### 直接使用Tesseract
这里介绍两种方法，一种是类似PyTesser的通过shell与tesseract通信完成识别过程；另一种是通过动态链接库（Windows下即DLL）实现。

#### shell
tesseract命令的格式为

`tesseract imagename outputbase [-l lang] [-psm pagesegmode] [configfile...]`

其中imagename为输入图片路径，outputbase为输出文本文件路径，此文本文件内容为图片文本识别结果。

所以通过shell实现的简单步骤就是

1.在Python中通过shell接口执行tesseract命令，指定输入和输出路径
2.读取输出文本文件内容
3.返回识别结果

#### 安装Tesseract
首先安装Tesseract，参考官方wiki。Linux下直接通过包管理器安装（如apt-get install tesseract）；Windows下3.02之后版本不提供安装包，但有一个3.05版的非官方安装包，点击这里直接下载，安装时记得展开“Registry settings”选项，在“Add to Path”前打钩。

安装完成后在shell中输入

`tesseract -v`
即可看到如下信息：
```
tesseract 3.05.00dev
 leptonica-1.73
  libgif 4.1.6(?) : libjpeg 8d (libjpeg-turbo 1.4.2) : libpng 1.6.20 : libtiff 4.0.6 : zlib 1.2.8 : libwebp 0.4.3 : libopenjp2 2.1.0
```
注意：安装得到的Tesseract自带英文语言包，本文仅演示英文效果；如需中文请自行下载中文语言包，并修改相关命令。


#### 封装
现在将Tesseract封装为一个Python函数。
```n
import os
import subprocess

def image_to_string(img, cleanup=True, plus=''):
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text
```
这里解决了之前代码使用os.popen()不等待返回的bug，subprocess.check_output()会等待tesseract命令运行完成再返回。

#### 运行
```
print(image_to_string('./phototest.tif'))  # 打印识别出的文本，删除txt文件
print(image_to_string('./phototest.tif', False))  # 打印识别出的文本，不删除txt文件
print(image_to_string('./phototest.tif', False, '-l eng'))  # 打印识别出的文本，不删除txt文件，同时提供高级参数
```
上述3中调用方式得到相同的结果。

#### DLL
通过动态链接库相对与shell方式有几个优点：

- 无需安装Tesseract（一般由自身自带DLL文件）
- 无需生成文本文件再读取，直接调用方法返回识别得到的字符串
- 更丰富的API支持
DLL方法即通过加载DLL文件，直接利用Tesseract C-API，在Python中调用此API完成识别。

#### DLL文件
DLL文件通常需要编译得到，编译Tesseract参考官方wiki。Linux下得到libtesseract.so，Windows下得到libtesseract.dll。

Windows下编译得到DLL文件也可以参考我的这篇文章：[Tesseract 3.05及之后版本编译生成动态链接库DLL](https://www.polarxiong.com/archives/Tesseract-3-05%E5%8F%8A%E4%B9%8B%E5%90%8E%E7%89%88%E6%9C%AC%E7%BC%96%E8%AF%91%E7%94%9F%E6%88%90%E5%8A%A8%E6%80%81%E9%93%BE%E6%8E%A5%E5%BA%93DLL.html)。

#### 封装和运行
对加载DLL和调用API作封装。

#### x86
```
import ctypes

DLL_PATH = 'C:/tesseract/build/bin/Release/tesseract305.dll'
TESSDATA_PREFIX = b'./tessdata'
lang = b'eng'

tesseract = ctypes.cdll.LoadLibrary(DLL_PATH)
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
if rc:
    tesseract.TessBaseAPIDelete(api)
    print('Could not initialize tesseract.\n')
    exit(3)


def from_file(path):
    tesseract.TessBaseAPIProcessPages(api, path, None, 0, None)
    text_out = tesseract.TessBaseAPIGetUTF8Text(api)
    return ctypes.string_at(text_out)

if __name__ == '__main__':
    image_file_path = b'./phototest.tif'
    result = from_file(image_file_path)
    print(result)
```
#### x64
```
import ctypes

DLL_PATH = 'C:/tesseract/build/bin/Release/tesseract305.dll'
TESSDATA_PREFIX = b'./tessdata'
lang = b'eng'

tesseract = ctypes.cdll.LoadLibrary(DLL_PATH)
tesseract.TessBaseAPICreate.restype = ctypes.c_uint64
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(ctypes.c_uint64(api), TESSDATA_PREFIX, lang)
if rc:
    tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
    print('Could not initialize tesseract.\n')
    exit(3)

def from_file(path):
    tesseract.TessBaseAPIProcessPages(
        ctypes.c_uint64(api), path, None, 0, None)
    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
    text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
    return ctypes.string_at(text_out)

if __name__ == '__main__':
    image_file_path = b'./phototest.tif'
    result = from_file(image_file_path)
    print(result)
```
关于对x86和x64进行区分的原因，参见我的另一篇文章Python x64下ctypes动态链接库出现access violation的原因分析。

关于更多的API调用方法，还请自行寻找。

### 小结
对比来说，shell方法和DLL方法各有优劣，但总的来说DLL方法更胜一筹，由于少了一次磁盘写入和读取，在性能上也更优。不管怎样，PyTesser实在是没有继续用下去的意义了。

在介绍DLL方法的时候本来想介绍直接向API传入图片数据（不读取文件）进行识别的，但折腾PIL库没有成功，不过网上倒有通过opencv成功的例子，但opencv太过重量级这里就不介绍了，感兴趣的话可以看参考链接。

### 参考
- [tesseract-ocr/tesseract: Tesseract Open Source OCR Engine (main repository)](https://github.com/tesseract-ocr/tesseract)
- [PyTesser Home Page](https://code.google.com/archive/p/pytesser/)
- [python - How to recognize data not filename using ctypes and tesseract 3.0.2? - Stack Overflow](http://stackoverflow.com/questions/13150937/how-to-recognize-data-not-filename-using-ctypes-and-tesseract-3-0-2)
- [opencv - Using C API of tesseract 3.02 with ctypes and cv2 in python - Stack Overflow](http://stackoverflow.com/questions/21745205/using-c-api-of-tesseract-3-02-with-ctypes-and-cv2-in-python?rq=1)


