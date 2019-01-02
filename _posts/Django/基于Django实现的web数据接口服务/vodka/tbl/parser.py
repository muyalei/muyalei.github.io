# -*- coding: utf-8 -*-
#encoding=utf-8
import re
import sys
import json
#from langconv import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def Extract(str, begin, end):
   rst = []
   l = len(str)
   s = 0
   while True:
     s = str.find(begin, s, l)
     if s == -1:
       break
     s += len(begin)
     e = str.find(end, s, l)
     if e == -1:
       break
     rst.append(str[s:e])
     s = e + len(end)

   return rst

def Transformation(g):
    if "万美元" in g:
        g=g.replace("万美元","")
        return float(g)*63000

    elif "万瑞士法郎" in g:
        g=g.replace("万瑞士法郎","")
        return float(g)*63880


    elif "万新加坡元" in g:
        g=g.replace("万新加坡元","")
        return float(g)*47693



    elif "万人民币元" in g:
        g=g.replace("万人民币元","")
        return float(g)*10000

    elif "万元人民币" in g:
        g=g.replace("万元人民币","")
        return float(g)*10000


    elif "万人民币" in g:
        g=g.replace("万人民币","")
        return float(g)*10000




    elif "万欧元" in g:
        g=g.replace("万欧元","")
        return float(g)*76471


    elif "万日元" in g:
        g = g.replace("万日元", "")
        return float(g) * 579.2098

    elif "人民币元" in g:
        g=g.replace("人民币元","")
        return float(g)
    elif "万港元" in g:
        g=g.replace("万港元","")
        return float(g) * 8068.4202
    elif "万英镑" in g:
        g=g.replace("万英镑","")
        return float(g) * 87040

    elif "万元" in g:
        g=g.replace("万元","")
        if "￥" in g:
            g = g.replace("￥", "")

            print g
        return float(g)*10000

    elif "万加元" in g:
        g=g.replace("万加元","")
        return float(g)*49422

    elif g=='-':
        g=0
        return g

    elif "万" in g:
        g=g.replace("万","")
        return float(g)*10000

    else:
        return g



#公司名中包含的全角括号转半角
def comName(g):
    if "（" in g:
        g=g.replace("（","(")


        if "）" in g:
            g=g.replace("）",")")

            if " " in g:
                g=g.replace(" ","")

    return g

def ReadCodeFromFile() :
  fp = open("test.txt", "r")
  rst = []
  for line in fp:
    line = line.strip()
    if len(line) == 0:
      continue
    rst.append(line)
  fp.close()

  return rst


#繁简体转换
def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line
def simple2tradition(line):
    #将简体转换成繁体
    line = Converter('zh-hant').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line
    
    
#企查查所属地区英文字母转换中文省名称
def Province(g):
    if g == "ZJ":
        g = g.replace("ZJ","浙江省")
        return g

    elif g == "AH":
        g = g.replace("AH","安徽省")
        return g

    elif g == "BJ":
        g = g.replace("BJ","北京市")
        return g

    elif g == "CQ":
        g = g.replace("CQ","重庆市")
        return g

    elif g == "FJ":
        g = g.replace("FJ","福建省")
        return g

    elif g == "GD":
        g = g.replace("GD","广东省")
        return g

    elif g == "GS":
        g = g.replace("GS","甘肃省")
        return g

    elif g == "GX":
        g = g.replace("GX","广西省")
        return g

    elif g == "GZ":
        g = g.replace("GZ","贵州省")
        return g

    elif g == "HAIN":
        g = g.replace("HAIN","海南省")
        return g

    elif g == "HB":
        g = g.replace("HB","河北省")
        return g

    elif g == "HEN":
        g = g.replace("HEN","河南省")
        return g

    elif g == "HK":
        g = g.replace("HK","香港特别行政区")
        return g

    elif g == "HLJ":
        g = g.replace("HLJ","黑龙江省")
        return g

    elif g == "HUB":
        g = g.replace("HUB","湖北省")
        return g


    elif g == "HUN":
        g = g.replace("HUN","湖南省")
        return g

    elif g == "JL":
        g = g.replace("JL", "吉林省")
        return g


    elif g == "JS":
        g = g.replace("JS", "江苏省")
        return g

    elif g == "JX":
        g = g.replace("JX", "江西省")
        return g


    elif g == "LN":
        g = g.replace("LN", "辽宁省")
        return g

    elif g == "NMG":
        g = g.replace("NMG", "内蒙古自治区")
        return g


    elif g == "NX":
        g = g.replace("NX", "宁夏回族自治区")
        return g

    elif g == "QH":
        g = g.replace("QH", "青海省")
        return g


    elif g == "SAX":
        g = g.replace("SAX", "陕西省")
        return g

    elif g == "SC":
        g = g.replace("SC", "四川省")
        return g


    elif g == "SD":
        g = g.replace("SD", "山东省")
        return g

    elif g == "SH":
        g = g.replace("SH", "上海市")
        return g


    elif g == "SX":
        g = g.replace("SX", "山西省")
        return g

    elif g == "TJ":
        g = g.replace("TJ", "天津市")
        return g


    elif g == "XJ":
        g = g.replace("XJ", "新疆维吾尔自治区")
        return g

    elif g == "XZ":
        g = g.replace("XZ", "西藏自治区")
        return g


    elif g == "YN":
        g = g.replace("YN", "云南省")
        return g


    else :
        return g