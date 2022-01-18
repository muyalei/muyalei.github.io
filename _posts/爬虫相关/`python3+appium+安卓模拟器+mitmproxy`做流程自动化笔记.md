---
layout: default
author: muyalei
title: `python3+appium+安卓模拟器+mitmproxy`做流程自动化笔记
date: 2021-09-28
tags:
	- 爬虫相关
---

# **鄙人原创，转载请注明出处**

**整理自：**

[https://www.cnblogs.com/soundcode/p/12682366.html](https://www.cnblogs.com/soundcode/p/12682366.html)

[https://www.cnblogs.com/grandlulu/p/9525417.html](https://www.cnblogs.com/grandlulu/p/9525417.html)

[https://www.jianshu.com/p/036e5057f0b9](https://www.jianshu.com/p/036e5057f0b9)

### Appium

#### 安装

- **安装`Android SDK`**

参考：[https://www.cnblogs.com/gufengchen/p/11038029.html](https://www.cnblogs.com/gufengchen/p/11038029.html)

- **安装Appium Python Client**

直接在命令提示窗口中输入`pip install Appium-Python-Client`

另外要确保安装匹配版本的selenium和appium：可以输入`pip install seelnium -U`

- **安装Appium Server**
  
  *两个都需要安装：*

  `Appium Desktop`用于定位app中的目标节点；

  npm安装版用于后台启动appium，流程自动化必备。代码实例：`os.system(r'start D:\xx\xx\appium.cmd')`或带参数（`appium –address 127.0.0.1 –port 4723 –no-reset –platform-name Android –platform-version 23 –automation-name Appium –log-no-color`）

  - Appium Desktop

  下载地址：[https://github.com/appium/appium-desktop/releases/tag/v1.15.1](https://github.com/appium/appium-desktop/releases/tag/v1.15.1)

  
  - node.js & npm

  安装node环境：[https://nodejs.org/en/download/](https://nodejs.org/en/download/)

  ```
  清理代理设置：
  npm config rm proxy
  npm config rm https-proxy 
  安装cnpm：
  npm install -g cnpm --registry=https://registry.npm.taobao.org
  通过cnpm安装appium、appium-doctor
  cnpm install -g appium@1.9.1
  cnpm install -g appium-doctor #可以不安装appium-doctor
  设置环境变量,默认应该是C:\Users\XXX\AppData\Roaming\npm\node_modules\cnpm\node_modules\.bin 加到PATH里
 
  不安装cnpm的话也可以修改npm配置：
  npm config set registry http://registry.npm.taobao.org
  改完之后查看是否改成功:
  npm config get registry
  之后就可以用npm安装了：
  npm install -g appium@1.9.1
  npm install -g appium-doctor #可以不安装
  耐心等待安装完成：
  appium -v 查看appium的版本
  appium-doctor 查看环境部署
  ```

- appium连接安卓模拟器代码实例（Nox）
```
desired_caps = {
	'platformName':'Android',
    'platformVersion':'7.1.2', #模拟器安卓版本
    'deviceName':device, #如`127.0.0.1:62001`
    'appPackage':'com.jingdong.app.mall', #使用`D:\Nox\bin\aapt dump badging xx.apk`查看
    'appActivity':'com.jingdong.app.mall.main.MainActivity', #同上
    'noReset':'True', #不清理缓存
    'unicodeKeyboard':'True', #向appium传入中文字符
    'resetKeyboard':'True' #向appium传入中文字符
}
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps) #`proxy`参数指定代理，示例：proxy={"http":'http://122.7.226.222:4258'}
robot_flow.wait = WebDriverWait(robot_flow.driver,30)
```

### mitmproxy

- **安装**

```
pip3 install mitmproxy
```
完成后，系统将拥有mitmproxy、mitmdump、mitmweb三个命令，mitmproxy命令不支持在 windows系统中运行。拿mitmdump测试一下安装是否成功：`mitmdump --version`

- *mitmproxy、mitmweb、mitmdump三者区别*

 - mitmproxy 命令启动后，会提供一个命令行界面，用户可以实时看到发生的请求，并通过命令过滤请求，查看请求数据。

 - mitmweb 命令启动后，会提供一个 web 界面，用户可以实时看到发生的请求，并通过 GUI 交互来过滤请求，查看请求数据。

 - mitmdump 命令启动后，没有界面，程序默默运行，无法提供过滤请求、查看数据的功能，只能结合自定义脚本，默默工作。（结合appium做流程自动化神器）

- **证书**

在cmd下运行`mitmdump`命令，以便在windows系统中产生CA证书。默认目录`C:\Users\用户名\.mitmproxy`
 
 - 在PC上安装证书

 mitmproxy-ca.p12 > 双击 > 当前用户 > 包括所有扩展属性 > 受信任的根证书颁发机构 > 是，完成安装。

 - 手机端安装证书（安卓）

 将证书发送到手机sdcard目录下：`adb connect 127.0.0.1:62001` > `adb push mitmproxy-ca-cert.pem /sdcard/Download`。手机端：设置 > 安全 > 从SD卡安装，完成安装。

- **流量处理脚本**

  - 编写一个py文件供mitmproxy加载，文件中定义了若干函数，这些函数实现了某些mitmproxy提供的事件，mitmproxy 会在某个事件发生时调用对应的函数：
  ```
  import mitmproxy.http
  from mitmproxy import ctx

  num = 0
  def request(flow: mitmproxy.http.HTTPFlow):
      global num
      num = num + 1
      ctx.log.info("We've seen %d flows" % num)
  ```

  - 编写一个py文件供mitmproxy加载，文件定义了变量addons，addons 是个数组，每个元素是一个类实例，这些类有若干方法，这些方法实现了某些mitmproxy提供的事件，mitmproxy 会在某个事件发生时调用对应的方法。这些类，称为一个个addon：
  ```
  import mitmproxy.http
  from mitmproxy import ctx

  class Counter:
      def __init__(self):
          self.num = 0

      def request(self, flow: mitmproxy.http.HTTPFlow):
          self.num = self.num + 1
          ctx.log.info("We've seen %d flows" % self.num)

  addons = [
      Counter()
  ]
  ```

 - 常用过滤
 ```
 #http.HTTPFlow 实例 flow
 flow.request.headers #获取所有头信息，包含Host、User-Agent、Content-type等字段
 flow.request.url #完整的请求地址，包含域名及请求参数，但是不包含放在body里面的请求参数
 flow.request.pretty_url #同flow.request.url目前没看出什么差别
 flow.request.host #域名
 flow.request.method #请求方式。POST、GET等
 flow.request.scheme #什么请求 ，如https
 flow.request.path # 请求的路径，url除域名之外的内容
 flow.request.get_text()  #请求中body内容，有一些http会把请求参数放在body里面，那么可通过此方法获取，返回字典类型
 flow.request.query #返回MultiDictView类型的数据，url直接带的键值参数
 flow.request.get_content()#bytes,结果如flow.request.get_text() 
 flow.request.raw_content #bytes,结果如flow.request.get_content()
 flow.request.urlencoded_form #MultiDictView，content-type：application/x-www-form-urlencoded时的请求参数，不包含url直接带的键值参数
 flow.request.multipart_form #MultiDictView，content-type：multipart/form-data 
 时的请求参数，不包含url直接带的键值参数
 #以上均为获取request信息的一些常用方法，对于response，同理
 flow.response.status_code #状态码
 flow.response.text#返回内容，已解码
 flow.response.content #返回内容，二进制
 flow.response.setText()#修改返回内容，不需要转码
 
 flow.request.url
 flow.request.host
 flow.request.headers
 flow.request.method
 if flow.request.method=='POST':
     flow.request.get_text() #获取表单数据'body'
 flow.response.headers
 flow.response.cookies
 flow.response.text #获取响应内容
 
 ```
 
 - 代码实例
 ```
 import json,mitmproxy.http
 from mitmproxy import ctx,http

 class Operation():
     def __init__(self):
         pass

     def request(self,flow:mitmproxy.http.HTTPFlow):
         if 'functionId=wareBusiness' in flow.request.url:
             pass

     def response(self,flow:mitmproxy.http.HTTPFlow):
         if 'functionId=wareBusiness' in flow.request.url:
             print('='*20)
             print(json.loads(flow.response.get_text()))
             print('='*20)
             with open('result.txt','a+',encoding='utf-8',errors='ignore') as f:
                 f.write(flow.response.get_text()+'\n$$$&&$$$\n')
                 f.close()

 addons = [
     Operation()
 ]
 ```

- **启动**
 ```
 mitmdump/mitmweb -p xx -s xx.py #指定监听端口、用于处理流量的脚本程序
 ```

- **更深入：事件**

mitmproxy的事件针对不同生命周期分为5类。`生命周期`这里指在哪一个层面看待事件，举例来说，同样是一次 web 请求，我可以理解为`HTTP请求>HTTP响应`的过程，也可以理解为`TCP连接>TCP通信>TCP断开`的过程。那么，如果我想拒绝来个某个IP的客户端请求，应当注册函数到针对TCP生命周期的tcp_start事件，又或者，我想阻断对某个特定域名的请求时，则应当注册函数到针对HTTP声明周期的http_connect事件。其他情况同理。

1. 针对HTTP生命周期

 - `def http_connect(self, flow: mitmproxy.http.HTTPFlow):`

 (Called when)收到了来自客户端的`HTTP CONNECT`请求。在flow上设置非2xx响应将返回该响应并断开连接。CONNECT 不是常用的HTTP请求方法，目的是与服务器建立代理连接，仅是client与proxy的之间的交流，所以CONNECT请求不会触发 request、response 等其他常规的HTTP事件。

 - `def requestheaders(self, flow: mitmproxy.http.HTTPFlow):`
 
 (Called when)来自客户端的HTTP请求的头部被成功读取。此时flow中的request的body是空的。

 - `def request(self, flow: mitmproxy.http.HTTPFlow):`
 
 (Called when)来自客户端的HTTP请求被成功完整读取。

 - `def responseheaders(self, flow: mitmproxy.http.HTTPFlow):`
 
 (Called when)来自服务端的HTTP响应的头部被成功读取。此时flow中的response的body是空的。

 - `def response(self, flow: mitmproxy.http.HTTPFlow):`
 
 (Called when)来自服务端端的HTTP响应被成功完整读取。

 - `def error(self, flow: mitmproxy.http.HTTPFlow):`
 
 (Called when)发生了一个HTTP错误。比如无效的服务端响应、连接断开等。注意与`有效的HTTP错误返回`不是一回事，后者是一个正确的服务端响应，只是`HTTP code`表示错误而已。

 2. 针对 TCP 生命周期、针对 Websocket 生命周期、针对网络连接生命周期、通用生命周期参考官方文档或[https://www.cnblogs.com/grandlulu/p/9525417.html](https://www.cnblogs.com/grandlulu/p/9525417.html)


### 模拟器

- **各种模拟器起连接方式**
```
神模拟器：adb connect 127.0.0.1:62001
逍遥安卓模拟器： adb connect 127.0.0.1:21503
天天模拟器：adb connect 127.0.0.1:6555
海马玩模拟器 ：adb connect 127.0.0.1:53001
网易MUMU模拟器：adb connect 127.0.0.1:7555
雷电模拟器：adb connect 127.0.0.1:5555

```

- **安装**

下载合适版本：[https://www.yeshen.com/blog/version/](https://www.yeshen.com/blog/version/)

用模拟器的`adb.exe`替换`android skd`中的`adb.exe`,目录位置示例：`D:\Android_SDK\platform-tools`

- **常用adb命令详解**

常用adb命令举例：
```
adb devices 
adb -s 127.0.0.1:62001 connect 
adb -s 127.0.0.1:62001 install/uninstall D:\\xx.apk
adb push D:\\xx.apk /sdcard/Download
adb pull /sdcard/Download D:\\xx.apk
adb shell am start -n 包名/Activity类名 #启动应用
adb shell am force-stop 包名 #关闭应用
```
*更多adb命令使用参考：*

[https://www.yeshen.com/faqs/H15tDZ6YW](https://www.yeshen.com/faqs/H15tDZ6YW)
[https://www.yeshen.com/faqs/B1cAyhMgb](https://www.yeshen.com/faqs/B1cAyhMgb)
[]()


### **流程自动化结束后退出appium、mitmproxy、安卓模拟器**

实例代码：
```
def quit():
    #杀死appium、mitmdump进程
    pid_list = list()
    process_appium = os.popen('netstat -ano | findstr "{port}"'.format(port=appium_port)).readlines()
    process_mitmdump = os.popen('netstat -ano | findstr "{port}"'.format(port=mitmdump_port)).readlines()
    for process in process_appium:
        pid_list.append(process.split(' ')[-1].replace('\n',''))
    for process in process_mitmdump:
        pid_list.append(process.split(' ')[-1].replace('\n',''))
    pid_list = list(set(pid_list))
    for pid in pid_list:
        if pid and int(pid)!=0:
            os.system('taskkill /pid {pid} /f'.format(pid=pid))
    os.system('taskkill /f /im cmd.exe') #关闭所有cmd窗口（appium退出后cmd窗口不自动关闭）
    os.system('D:\\夜神安卓模拟器\\Nox\\bin\\NoxConsole.exe quit -name:夜神模拟器2')
    print('退出appium、mitmproxy、nox完成')
```

### 完整项目实例代码

```
import datetime,os,pathlib
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os,traceback,random
from functools import wraps
from config import device,retryTimes_max,rebootTimes_max,appium_port,mitmdump_port,quit



#函数异常时用于重试的装饰器
def on_exception_retry(retryTimes_max):
    def retry_decorator(func):
        @wraps(func)
        def wrapped_function(*args,**kwargs):
            retryTimes_current = 1
            while retryTimes_current<=retryTimes_max:
                try:
                    return func(*args,**kwargs)
                except Exception:
                    print('retrying %s (failed %s times)\n' % (func.__name__,retryTimes_current))
                    print(traceback.print_exc())
                    retryTimes_current += 1
            print('give up retrying %s (failed %s times)' % (func.__name__,retryTimes_current))
            raise Exception('error retrying function %s' % (func.__name__))
        return wrapped_function
    return retry_decorator


class RobotFlow():
    def __init__(self):
        self.desired_caps = {
            'platformName':'Android',
            'platformVersion':'7.1.2',
            'deviceName':device,
            'appPackage':'com.jingdong.app.mall',
            'appActivity':'com.jingdong.app.mall.main.MainActivity',
            'noReset':'True', #不清理缓存
            'unicodeKeyboard':'True', #向appium传入中文字符
            'resetKeyboard':'True' #向appium传入中文字符
        }
        self.count = 0 #已抓取商品数量

    #直接搜索skuId
    def get_data(self,waitCrawl_list):
        try:
            time.sleep(5)
            self.driver.find_element_by_id('com.jingdong.app.mall:id/mj').click()
            print('出现广告遮蔽页，成功点掉')
        except Exception:
            pass
        #通过搜索框进入summary页面
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[3]/android.widget.ViewFlipper'))).click()
        for skuId in waitCrawl_list:
            self.wait.until(EC.element_to_be_clickable((By.ID,'com.jd.lib.search.feature:id/a3g'))).send_keys(skuId)
            self.wait.until(EC.element_to_be_clickable((By.ID,'a9b'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]'))).click()
            self.driver.back()
            self.wait.until(EC.element_to_be_clickable((By.ID,'com.jd.lib.search.feature:id/xu'))).clear()
            with open('done.txt','a+',encoding='utf-8',errors='ignore') as f:
                f.write(str(skuId)+'\n')
                f.close()
            self.count += 1
            print('已抓取数量：%s' % str(self.count))

    def get_waitCrawl_list(self):
        if not os.path.exists('skuId.txt'):
            print('没有找到文件`skuId.txt`，程序退出！！')
            sys.exit()
        if not os.path.exists('done.txt'):
            pathlib.Path('done.txt').touch()
        #读取全部商品skuId列表
        with open('skuId.txt','r',encoding='utf-8',errors='ignore') as f:
            skuId_list = f.read().split('\n')
            f.close()
        #读取已抓完的skuId列表文件
        with open('done.txt','r',encoding='utf-8',errors='ignore') as f:
            done_list = f.read().split('\n')
            f.close()
        waitCrawl_list = set(skuId_list)-set(done_list)
        print('待抓取商品数：%s' % len(waitCrawl_list))
        return waitCrawl_list

    #执行抓取动作
    def run(self):
        count = 0
        while count<retryTimes_max:
            try:
                waitCrawl_list = self.get_waitCrawl_list()
                if waitCrawl_list:
                    self.get_data(waitCrawl_list)
                    return True
                else:
                    print('待抓取商品skuId已经在`done.txt`中全部存在！！')
                    return True
            except Exception:
                print(traceback.print_exc())
                count += 1
                os.system('D:\\夜神安卓模拟器\\Nox\\bin\\nox_adb.exe shell am force-stop com.jingdong.app.mall') #关闭app
                os.system('D:\\夜神安卓模拟器\\Nox\\bin\\nox_adb.exe shell am start -n com.jingdong.app.mall/com.jingdong.app.mall.main.MainActivity') #启动应用



def main():
    #开始抓取
    print('开始抓取...')
    count = 0
    while count<=rebootTimes_max:
        try:
            os.system('D:\\夜神安卓模拟器\\Nox\\bin\\NoxConsole.exe launch -name:夜神模拟器2') #启动模拟器
            time.sleep(30) #等待模拟器启动完成
            print('模拟器启动完成')
            robot_flow.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',robot_flow.desired_caps)
            robot_flow.wait = WebDriverWait(robot_flow.driver,30)
            robot_flow.run() #抓取流程正常走完，返回True
            print('抓取完成')
            break
        except Exception:
            print(traceback.print_exc())
            os.system('D:\\夜神安卓模拟器\\Nox\\bin\\NoxConsole.exe quit -name:夜神模拟器2') #退出模拟器
            #os.system('D:\\夜神安卓模拟器\\Nox\\bin\\NoxConsole.exe launch -name:夜神模拟器2') #启动模拟器
            #os.system('D:\\夜神安卓模拟器\\Nox\\bin\\NoxConsole.exe reboot -name:夜神模拟器2') #重启模拟器
            count += 1
    if count>rebootTimes_max:
        print('超过模拟器最大重启次数，抓取失败！！')
    else:
        #清空`done.txt`
        with open('done.txt','r+') as f:
            f.truncate()
            f.close()


if __name__=='__main__':
    try:
        quit() #确定appium、mitmdump已经退出，避免因为端口被占用报错
        os.system(r'start D:\nodejs\node\node_modules\.bin\appium.cmd') #后台启动appium
        print('开启appium成功')
        os.system(r'start mitmdump -p8888 -s mitmproxy.py') #后台启动mitmproxy
        print('开启mitmdump成功')
        robot_flow = RobotFlow()
        main()
        robot_flow.driver.quit()
    except Exception:
        print(traceback.print_exc())
    finally:
        quit() #退出appium、mitmdump
```

