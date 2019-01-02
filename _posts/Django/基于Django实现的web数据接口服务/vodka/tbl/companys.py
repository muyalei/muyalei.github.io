# -*- coding: utf-8 -*-
from __future__ import division
from lxml import etree
import MySQLdb
from lxml import html
import requests
from urllib import quote
from urllib import unquote
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.http import urlquote
import string
import json,sys,logging
reload(sys)
sys.setdefaultencoding('utf-8')
import parser
from  proxies_abuyun import get_abuyun_proxies
sys.path.append("..")
import dianping.config
import time
import math
import hashlib


#企查查参数
appKey = '0da3829cdad6414b9b39623c70952cc8'
SecretKey = '49B1D715566BFD92B3CAE4840B24F682'

#生成加密token
def md5_crypt(txt):
    m = hashlib.md5()
    m.update(txt.encode())
    return m.hexdigest().upper()


logger = logging.getLogger('dianping.tbl.companys')

#获取搜索结果列表页
def summary(request):
    logger.info(request)

    p = request.GET.get('page_num')
    key = request.GET.get('key')
    print p,key

    if not key:
        error_msg = {'errorCode': '404', 'errorMsg': 'key参数有误','companies':[]}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))
    if p is None:
        error_msg = {'errorCode': '404', 'errorMsg': 'page_num参数有误','companies':[]}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))

    Timespan = str(int(time.time()))
    Token = md5_crypt(appKey+Timespan+SecretKey)

    headers = {
        'Token':Token,
        'Timespan':Timespan
    }

    url = "http://api.qichacha.com/ECIV4/Search"
    querystring = {"key": "0da3829cdad6414b9b39623c70952cc8","dtype":"json","keyword":key,"pageSize":20, "pageIndex": p}


    response = requests.request("GET", url,  params=querystring,headers=headers).text
    #with open("comList", "a") as f:
        #f.write(response)

    if 'Status":"201","Message":"查询无结果"' in response:
        error_msg = {'errorCode': '201', 'errorMsg': '无查询结果', 'companies': []}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))

    if 'Status":"203"' in response:
        error_msg = {'errorCode': '203', 'errorMsg': '企查查接口服务异常', 'companies': []}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))

    datas = json.loads(response)
    PageSize = datas['Paging']['PageSize']
    TotalRecords = datas['Paging']['TotalRecords']
    ad =  TotalRecords / PageSize
    pages = math.ceil(ad)
    company = datas['Result']
    dir(company)
    result = {'errorCode': '200', 'errorMsg': 'success!', 'total_pages': pages, 'companies': company}
    return HttpResponse(json.dumps(result, ensure_ascii=False))

#获取公司详细信息
def detail(request):
    logger.info(request)
    #获取客户端传过来的com_id
    com_id = request.GET.get('com_id')
    if not com_id:
        error_msg = {'errorCode': '404', 'errorMsg': 'com_id参数有误','companies':[]}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))
    com_id = com_id.strip()
    if len(com_id) !=32:
        error_msg = {'errorCode': '401', 'errorMsg': '请输入合法的公司ID', 'companies': []}
        return HttpResponse(json.dumps(error_msg, ensure_ascii=False))

    # 连接数据库
    conn = MySQLdb.connect(
        host=dianping.config.HOST,
        db='db_mdc',
        user=dianping.config.USER,
        passwd=dianping.config.PASSWORD,
        charset='utf8',
        port=dianping.config.PORT
    )
    print " DB conection is %s" % dianping.config.HOST,dianping.config.USER,dianping.config.PASSWORD,dianping.config.PORT
    conn.select_db('db_mdc')
    cur = conn.cursor()

    #根据客户端传过来的com_id ,去MDC库里查询公司信息
    sql1 = "SELECT companyID,companyName,logo,legalRepresentative,registeredCapital,contributedCapital,operatingState,establishDay,registerNum,organizationCode,creditNum,taxpayerNum,companyType,industry,approvalDay,registrationAuthority,affiliatedArea,englishName,oldName,operationMode,peopleNum,closingDay,address,operationScope FROM db_mdc.tbl_company_info where companyID = "
    cur.execute( sql1 + "\'" + com_id + "\'");
    results = cur.fetchall()

    #如果该公司在MDC里存在相关信息，继续查该公司的品牌信息
    if len(results)>0:
        sql2 = "select brandName from db_mdc.tbl_brand_company where companyID ="
        cur.execute(sql2 + "\'" + com_id + "\'");
        results2 = cur.fetchall()

        #存com_id对应的品牌
        brand_name = []
        for r2 in results2:
            bd = ','.join(r2)
            brand_name.append(bd)
        brand_name=','.join(brand_name)

    #存MDC中查询到的公司信息
    for r in results:
        companyID = r[0]
        companyName = r[1]
        logo = r[2]
        legalRepresentative = r[3]
        registeredCapital = r[4]
        contributedCapital = r[5]
        operatingState = r[6]
        establishDay = r[7]
        registerNum = r[8]
        organizationCode = r[9]
        creditNum = r[10]
        taxpayerNum = r[11]
        companyType = r[12]
        industry = r[13]
        approvalDay = r[14]
        registrationAuthority = r[15]
        affiliatedArea = r[16]
        englishName = r[17]
        oldName = r[18]
        operationMode = r[19]
        peopleNum = r[20]
        closingDay = r[21]
        address = r[22]
        operationScope = r[23]

        dic = {"companyID":companyID,"companyName":companyName,"logo":logo,"legalRepresentative":legalRepresentative,"registeredCapital":registeredCapital,\
               "contributedCapital":contributedCapital,"operatingState":operatingState,"establishDay":establishDay,"registerNum":registerNum,\
               "organizationCode":organizationCode,"creditNum":creditNum,"taxpayerNum":taxpayerNum,"taxpayerNum":taxpayerNum,"companyType":companyType,\
               "industry":industry,"approvalDay":approvalDay,"registrationAuthority":registrationAuthority,"affiliatedArea":affiliatedArea,"englishName":englishName,\
               "oldName":oldName,"operationMode":operationMode,"peopleNum":peopleNum,"closingDay":closingDay,"address":address,"operationScope":operationScope,"brandName":brand_name}

        results = {'errorCode': '200', 'errorMsg': 'success!','companyInfo': dic}

        return HttpResponse(json.dumps(results, ensure_ascii=False))


    #如果库里不存在该com_id对应的公司，调企查查API
    else:

        Timespan = str(int(time.time()))
        Token = md5_crypt(appKey + Timespan + SecretKey)

        headers = {
            'Token': Token,
            'Timespan': Timespan
        }

        url = "http://api.qichacha.com/ECIV4/GetDetailsByName?key=0da3829cdad6414b9b39623c70952cc8&keyword=" + com_id
        response = requests.request("GET", url, headers=headers).text

        #with open("details.txt", "a") as f:
            #f.write('\n'+response)
        if 'Status":"201","Message":"查询无结果"' in response:
            error_msg = {'errorCode': '201', 'errorMsg': '暂无相关数据','companies':[]}
            return HttpResponse(json.dumps(error_msg, ensure_ascii=False))
            
        if '"Status":"208","Message":"请求数据过旧，系统正在更新' in response:
            error_msg = {'errorCode': '208', 'errorMsg': '请求数据过旧，企查查API正在更新','companies':[]}
            return HttpResponse(json.dumps(error_msg, ensure_ascii=False))

        datas = json.loads(response)

        if datas['Result']['Industry'] is None:
            industry = '-'
        elif datas['Result']['Industry']['Industry'] is None:
            industry = '-'
        else:
            industry = datas['Result']['Industry']['Industry']

        companyID = datas['Result']['KeyNo']
        companyName = datas['Result']['Name']
        if companyName is None:
            companyName = '-'

        url = "http://www.qichacha.com/firm_" + companyID + ".html"
        legalRepresentative = datas['Result']['OperName']
        if legalRepresentative is None:
            legalRepresentative ='-'

        registeredCapitals = datas['Result']['RegistCapi']
        if registeredCapitals is None:
            registeredCapital = 0
        else:
            registeredCapital = parser.Transformation(registeredCapitals) #将货币单位统一转换成人民币（元）

        contributedCapital = '' #企查查API返回无此字段，需后期抓取
        operatingState = datas['Result']['Status']
        if operatingState is None:
            operatingState = '-'

        establishDay = datas['Result']['StartDate']
        if establishDay is None:
            establishDay = '-'
        establishDay = establishDay.replace("T00:00:00+08:00","")

        registerNum = datas['Result']['No']
        if registerNum is None:
            registerNum = '-'

        organizationCode = datas['Result']['OrgNo']
        if organizationCode is None:
            organizationCode = '-'

        taxpayerNum = datas['Result']['CreditCode']
        if taxpayerNum is None:
            taxpayerNum = '-'

        creditNum = datas['Result']['CreditCode']
        if creditNum is None:
            creditNum ='-'

        companyType = datas['Result']['EconKind']
        if companyType is None:
            companyType = '-'

        approvalDay = datas['Result']['CheckDate']
        if approvalDay is None:
            approvalDay = '-'
        approvalDay = approvalDay.replace("T00:00:00+08:00","")

        registrationAuthority = datas['Result']['BelongOrg']
        if registrationAuthority is None:
            registrationAuthority = '-'

        affiliatedArea = datas['Result']['Province']
        if affiliatedArea is None:
            affiliatedArea = '-'
        affiliatedArea = parser.Province(affiliatedArea) #需人工录入省份代码

        englishName = ''

        oldNames = datas['Result']['OriginalName'] #需要再次处理
        if oldNames is None:
            oldName ='-'
        else:
            sd = []
            for on in oldNames:
                oldName = on['Name']
                sd.append(oldName)
            oldName = ','.join(sd)

        operationMode = ''
        peopleNum = ''
        closingDay1 = datas['Result']['TermStart']
        closingDay2 = datas['Result']['TeamEnd']
        if closingDay1 or closingDay2  is None:
            closingDay = "*** 至 无固定期限"
        else:
            closingDay = closingDay1.replace("T00:00:00+08:00","") + "至"+ closingDay2.replace("T00:00:00+08:00","")
        address = datas['Result']['Address']
        if address is None:
            address = '-'

        operationScope = datas['Result']['Scope']
        if operationScope is None:
            operationScope = '-'

        brandName = '' #企查查API返回无此字段，需后期抓取
        logo = '' #企查查API返回无此字段，需后期抓取
        type = -1 #企查查API返回的数据，非爬虫抓取



        
        # 将企查查API数据写入详情表db_mdc_company_raw.tbl_qcc_details
        try:

            sql3 ='insert into db_mdc_company_raw.tbl_qcc_details (logo,type,url,companyName,legalRepresentative,registeredCapital,contributedCapital,operatingState,establishDay,registerNum,organizationCode,taxpayerNum,creditNum,companyType,industry,approvalDay,registrationAuthority,affiliatedArea,englishName,oldName,operationMode,peopleNum,closingDay,address,operationScope) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")'% (logo,type,url, companyName, legalRepresentative, registeredCapital, contributedCapital, operatingState,establishDay, registerNum, organizationCode, taxpayerNum, creditNum, companyType, industry,approvalDay, registrationAuthority, affiliatedArea, englishName, oldName, operationMode, peopleNum,closingDay, address, operationScope)
            cur = conn.cursor()
            cur.execute(sql3)
            conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])



        dic = {"companyID": com_id, "companyName": companyName,"logo": logo,
               "legalRepresentative": legalRepresentative, "registeredCapital": registeredCapital, \
               "contributedCapital": contributedCapital, "operatingState": operatingState, "establishDay": establishDay,
               "registerNum": registerNum, \
               "organizationCode": organizationCode, "creditNum": creditNum, "taxpayerNum": taxpayerNum,
               "taxpayerNum": taxpayerNum, "companyType": companyType, \
               "industry": industry, "approvalDay": approvalDay, "registrationAuthority": registrationAuthority,
               "affiliatedArea": affiliatedArea, "englishName": englishName, \
                "operationMode": operationMode, "peopleNum": peopleNum,
               "address": address, "operationScope": operationScope, "brandName": brandName,"oldName":oldName,"closingDay":closingDay}
        results = {'errorCode': '200', 'errorMsg': 'success!', 'companyInfo': dic}

        return HttpResponse(json.dumps(results, ensure_ascii=False))




