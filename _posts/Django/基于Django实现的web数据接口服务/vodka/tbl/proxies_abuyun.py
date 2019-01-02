# -*- coding: utf-8 -*-
from lxml import etree
import MySQLdb
from lxml import html
import requests
from urllib import quote
from urllib import unquote
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.http import urlquote
import string
import json,sys
reload(sys)
sys.setdefaultencoding('utf-8')


#获取 阿布云 代理url
def get_abuyun_proxies():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H46U7S8E21V5FE7D"
    proxyPass = "E6EBE6181904EE7C"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

