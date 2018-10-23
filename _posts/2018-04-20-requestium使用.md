---
layout:     post
title:      requestium使用
subtitle:   requestium
date:       2018-04-20
author:     muyalei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - requestium
    - selenium
---

### 实例样本
```
class Spider(object):
    s = Session(webdriver_path='chromedriver',  #需要安装chromedriver，并将chromedriver所在目录添加进环境变量
                browser='chrome',  
                default_timeout=30,
                webdriver_options={'arguments':['headless']}) #不加载交互界面，提高效率

    def __init__(self):
        pass

    #获取请求参数，主要是js加密生成的siTag参数
    def get_params(self):
        try:
            self.s.driver.get('https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E4%BC%9A%E8%AE%A1')
            self.s.driver.ensure_element_by_link_text('下一页',state='clickable',timeout=30).ensure_click()
            print(self.s.driver.current_url)
            ckid = re.search(r'ckid=(.*?)&',self.s.driver.current_url,re.S).group(1)
            siTag = re.search(r'siTag=(.*?)&',self.s.driver.current_url,re.S).group(1)
            d_ckid = re.search(r'd_ckId=(.*?)&',self.s.driver.current_url,re.S).group(1)
            self.s.driver.quit() #成功获取到目标参数字段后，关闭webdriver
            return ckid,siTag,d_ckid
        except Exception as e:
            time.sleep(3)
            self.get_params()
            print('get_params()请求失败！错误信息：%s' % str(e.args))
```

### github主页
https://github.com/tryolabs/requestium

