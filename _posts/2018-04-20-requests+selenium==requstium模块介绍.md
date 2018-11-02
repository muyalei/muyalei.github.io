---
layout: deault
author: muyalei
date: 2018-04-20
title: requests+selenium==requestium模块介绍
tags:
   - python模块
---

有时，你可能会在网上实现一些自动化操作。比如抓取网站，进行应用测试，或在网上填表，但又不想使用API，这时自动化就变得很必要。Python提供了非常优秀的Requests库可以辅助进行这些操作。可惜，很多网站采用基于JavaScript的重客户端，这就意味着Requests获取的HTML代码中根本就没有用来自动化操作的表单，更别提自动填表了！它取回的基本上都是React或Vue这些现代前端库在浏览器中生成的空DIV这类的代码。

虽然可以通过反向工程处理JavaScript生成的代码，但这需要花几个小时来编译。处理这些丑陋的JS代码，谢谢，还是算了吧。还有一个方法就是使用Selenium库，允许以程序化的方式和浏览器进行交互，并运行JavaScript代码。用了这个库就没什么问题了，但它比占用资源极少的Requests慢太多了。

如果能以Requests为主，只在需要Selenium的时候才无缝调用，这样不是更好？看看Requestium吧，它以内嵌方式取代Requests，而且干的不错。它整合了Parsel，用它编写的页面查询元素选择器代码特别清晰，它还为诸如点击元素和在DOM中渲染内容这些通用操作提供了帮助。又一个网页自动化省时利器！

#### 安装

`pip install requestium`

然后你应该下载您的首选是WebDriver如果你计划使用Requestium的selenium的一部分：Chromedriver或PhantomJS

#### 使用

首先创建一个会话，你可以请求，并且可以随意地添加参数的网络驱动程序
```
from requestium import Session, Keys

s = Session(webdriver_path='./chromedriver',
            browser='chrome',
            default_timeout=15,
            webdriver_options={'arguments': ['headless']})
```

你不需要解析的响应，它是自动完成时调用XPath，CSS或re

`title = s.get('http://samplesite.com').xpath('//title/text()').extract_first(default='Default Title')`

正则表达式需要较少的样本相比，Python的标准re模块
```
response = s.get('http://samplesite.com/sample_path')

# Extracts the first match
identifier = response.re_first(r'ID_\d\w\d', default='ID_1A1')

# Extracts all matches as a list
users = response.re(r'user_\d\d\d')
```

会话对象只是一个普通的请求的会话对象，所以你可以使用所有的方法。
```
s.post('http://www.samplesite.com/sample', data={'field1': 'data1'})
s.proxies.update({'http': 'http://10.11.4.254:3128', 'https': 'https://10.11.4.252:3128'})
```
你可以切换使用的是WebDriver运行任何JS代码。
```
s.transfer_session_cookies_to_driver()  # You can maintain the session if needed
s.driver.get('http://www.samplesite.com/sample/process')
```
驱动对象是一个是WebDriver的对象，所以你可以使用任何正常selenium方法加上新添加的requestium方法。
```
s.driver.find_element_by_xpath("//input[@class='user_name']").send_keys('James Bond', Keys.ENTER)

# New method which waits for element to load instead of failing, useful for single page web apps
s.driver.ensure_element_by_xpath("//div[@attribute='button']").click()
```
requestium还增加了XPath，CSS，和re作为selenium的驱动对象。
```
if s.driver.re(r'ID_\d\w\d some_pattern'):
    print('Found it!')
```
最后你可以切换回用要求。
```
s.transfer_driver_cookies_to_session()
s.post('http://www.samplesite.com/sample2', data={'key1': 'value1'})
```
你可以使用这些元素的方法有新的ensure_click方法是点击不易失败。这有助于通过大量的selenium点击问题。
```
s.driver.ensure_element_by_xpath("//li[@class='b1']", state='clickable', timeout=5).ensure_click()

# === We also added these methods named in accordance to Selenium's api design ===
# ensure_element_by_id
# ensure_element_by_name
# ensure_element_by_link_text
# ensure_element_by_partial_link_text
# ensure_element_by_tag_name
# ensure_element_by_class_name
# ensure_element_by_css_selector

add cookie

cookie = {"domain": "www.site.com",
          "secure": false,
          "value": "sd2451dgd13",
          "expiry": 1516824855.759154,
          "path": "/",
          "httpOnly": true,
          "name": "sessionid"}
s.driver.ensure_add_cookie(cookie, override_domain='')
```
#### 使用requestium
```
from requestium import Session, Keys

# If you want requestium to type your username in the browser for you, write it in here:
reddit_user_name = ''

s = Session('./chromedriver', browser='chrome', default_timeout=15)
s.driver.get('http://reddit.com')
s.driver.find_element_by_xpath("//a[@href='https://www.reddit.com/login']").click()

print('Waiting for elements to load...')
s.driver.ensure_element_by_class_name("desktop-onboarding-sign-up__form-toggler",
                      state='visible').click()

if reddit_user_name:
    s.driver.ensure_element_by_id('user_login').send_keys(reddit_user_name)
    s.driver.ensure_element_by_id('passwd_login').send_keys(Keys.BACKSPACE)
print('Please log-in in the chrome browser')

s.driver.ensure_element_by_class_name("desktop-onboarding__title", timeout=60, state='invisible')
print('Thanks!')

if not reddit_user_name:
    reddit_user_name = s.driver.xpath("//span[@class='user']//text()").extract_first()

if reddit_user_name:
    s.transfer_driver_cookies_to_session()
    response = s.get("https://www.reddit.com/user/{}/".format(reddit_user_name))
    cmnt_karma = response.xpath("//span[@class='karma comment-karma']//text()").extract_first()
    reddit_golds_given = response.re_first(r"(\d+) gildings given out")
    print("Comment karma: {}".format(cmnt_karma))
    print("Reddit golds given: {}".format(reddit_golds_given))
else:
    print("Couldn't get user name")
```
使用Requests + Selenium + lxml
```
import re
from lxml import etree
from requests import Session
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# If you want requestium to type your username in the browser for you, write it in here:
reddit_user_name = ''

driver = webdriver.Chrome('./chromedriver')
driver.get('http://reddit.com')
driver.find_element_by_xpath("//a[@href='https://www.reddit.com/login']").click()

print('Waiting for elements to load...')
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "desktop-onboarding-sign-up__form-toggler"))
).click()

if reddit_user_name:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'user_login'))
    ).send_keys(reddit_user_name)
    driver.find_element_by_id('passwd_login').send_keys(Keys.BACKSPACE)
print('Please log-in in the chrome browser')

try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "desktop-onboarding__title"))
    )
except TimeoutException:
    pass
WebDriverWait(driver, 60).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "desktop-onboarding__title"))
)
print('Thanks!')

if not reddit_user_name:
    tree = etree.HTML(driver.page_source)
    try:
        reddit_user_name = tree.xpath("//span[@class='user']//text()")[0]
    except IndexError:
        reddit_user_name = None

if reddit_user_name:
    s = Session()
    # Reddit will think we are a bot if we have the wrong user agent
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    s.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    response = s.get("https://www.reddit.com/user/{}/".format(reddit_user_name))
    try:
        cmnt_karma = etree.HTML(response.content).xpath(
            "//span[@class='karma comment-karma']//text()")[0]
    except IndexError:
        cmnt_karma = None
    match = re.search(r"(\d+) gildings given out", str(response.content))
    if match:
        reddit_golds_given = match.group(1)
    else:
        reddit_golds_given = None
    print("Comment karma: {}".format(cmnt_karma))
    print("Reddit golds given: {}".format(reddit_golds_given))
else:
    print("Couldn't get user name")
```

参考：
- [https://github.com/tryolabs/requestium] 
- [https://pypi.python.org/pypi/requestium] 
- [http://www.cnblogs.com/botoo/p/8327762.html]
