#/usr/bin/python 
# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from . models import Basic_shop_info,China_businessarea,Dianping_cuisine
import json,sys,logging

reload(sys)
sys.setdefaultencoding('utf-8')


logger = logging.getLogger('dianping.tbl.views')

#首页
def index(request):
    return HttpResponse('Hello,world~')


#根据给出的店铺名称，查询数据库（模糊查询）
def summary(request):
    logger.info(request)
    shop_name = request.GET.get('shop_name')
    city = request.GET.get('city')
    
    if not shop_name and not city:
        error_msg = {'errorCode': '404','errorMsg':'shop_name、city参数缺失！请输入完整查询参数，如：?shop_name=小吃&city=北京市（或city=北京）','shops':[]}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))
    elif not shop_name:
        error_msg = {'errorCode':'404','errorMsg':'shop_name参数缺失！请输入完整查询参数，如：?shop_name=小吃&city=北京市（或city=北京）','shops':[]}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))
    elif not city:
        error_msg = {'errorCode': '404','errorMsg':'city参数缺失！请输入完整查询参数，如：?shop_name=小吃&city=北京市（或city=北京）','shops':[]}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))

    #根据待查询的店铺名进行模糊查询
    items = Basic_shop_info.objects.filter(city__icontains=city).filter(shopName__icontains=shop_name)
    if not items:
        result = {'errorCode':'404','errorMsg':'没有查询到该店铺信息！','shops':[]}
    else:
        shopList = list() #所有查询到的店铺写入一个列表
        for item in items:
            shopList.append({'shopID':item.shopID,'shopName':item.shopName,'address':item.address}) #命中店铺的集合
        result = {'errorCode':'200','errorMsg':'success','shops':shopList}

    return HttpResponse(json.dumps(result,ensure_ascii=False))


#根据给出的店铺id，查询数据库（模糊查询）
def detail(request):
    logger.info(request)
    shop_id = request.GET.get('shop_id')

    if not shop_id:
        error_msg = {'errorCode':'404','errorMsg':'请输入店铺id!'}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))

    #根据待查询的店铺名进行模糊查询
    item = Basic_shop_info.objects.filter(shopID=shop_id) #注意：filter过滤后返回的结果是一个list！！
    if not item:
        result = {'errorCode':'404','errorMsg':'没有查询到该店铺信息！'}
    else:
        item = item[0]
        shop_info = dict() #每个店铺的基本信息
        shop_info['shopID'] = item.shopID
        shop_info['shopName'] = item.shopName
        shop_info['city'] = item.city
        shop_info['address'] = item.address
        shop_info['shopLogo']= item.shopLogo
        shop_info['position'] = item.position
        shop_info['mapAddr'] = item.mapAddr
        shop_info['telephone'] = item.telephone
        shop_info['businessTime'] = item.businessTime
        shop_info['avgPrice'] = str(item.avgPrice)

        result = {'errorCode':'200','errorMsg':'success','shopInfo':shop_info}
    
    return HttpResponse(json.dumps(result,ensure_ascii=False))


#更新店铺信息
def feedback(request):
    logger.info(request)
    errors = []
    if request.method=='POST':
        if not request.POST.get('id',''):
            errors.append('Enter a id.')
        if not request.POST.get('name',''):
            errors.append('Enter a name.')
        if not request.POST.get('city',''):
            errors.append('Enter a city.')
        if not request.POST.get('address',''):
            errors.append('Enter a address.')
        if not request.POST.get('phone',''):
            errors.append('Enter a phone.')
        if not request.POST.get('businessTime',''):
            errors.append('Enter a businessTime.')
        if not request.POST.get('avgPrice',''):
            errors.append('Enter a avgPrice.')
        if not request.POST.get('position',''):
            errors.append('Enter a position.')
        if errors:
            result = {'errorCode':'500','errorMsg':errors}
            return HttpResponse(json.dumps(result,ensure_ascii=False))
        else:
            #保存到mysql
            action = Basic_shop_info(
                shopID = request.POST['id'],
                shopName = request.POST['name'],
                city = request.POST['city'],
                address = request.POST['address'],
                telephone = request.POST['phone'],
                businessTime = request.POST['businessTime'],
                avgPrice = request.POST['avgPrice'],
                position = request.POST['position'],
            )
            action.save()
            return HttpResponseRedirect('results/')
    else:
        result = {'errorCode':'500','errorMsg':'当前请求是GET请求！'}
        return HttpResponse(json.dumps(result,ensure_ascii=False))

#确认提交接口
def confirm(request):
    logger.info(request)
    errors = []
    if request.method=='POST':
        if not request.POST.get('dpID',''):
            errors.append('Enter a dpID.')
        if not request.POST.get('hllShopID',''):
            errors.append('Enter a hllShopID.')
        if not request.POST.get('hllShopName',''):
            errors.append('Enter a hllShopName.')
        if errors:
            result = {'errorCode':'500','errorMsg':errors}
            return HttpResponse(json.dumps(result,ensure_ascii=False))
        else:
            #保存到mysql
            action = Basic_shop_info(
                shopID = request.POST['dpID'],
                hllShopID = request.POST['hllShopID'],
                hllShopName = request.POST['hllShopName'],
            )
            action.save()
            return HttpResponseRedirect('results/')
    else:
        result = {'errorCode':'500','errorMsg':'当前请求是GET请求！'}
        return HttpResponse(json.dumps(result,ensure_ascii=False))


def results(request):
    logger.info(request)
    result = {'errorCode':'200','errorMsg':'success!'}
    return HttpResponse(json.dumps(result,ensure_ascii=False))



#查询省市区商圈列表
def queryAreaList(request):
    items = China_businessarea.objects.all() #从tbl_china_businessarea中提取每一行记录

    #从tbl_china_businessarea中读取每一行记录，
    data = list()
    regionDict = dict()
    cityDict = dict()
    provinceDict = dict()
    provinceList = list()
    for item in items:
        provinceName = item.provinceName
        provinceCode = item.provinceCode
        cityName = item.cityName
        cityCode = item.cityCode
        countyName = item.countyName
        countyCode = item.countyCode
        businessAreaCode = item.id
        businessAreaName = item.businessAreaName

        info = {'provinceCode':provinceCode,'provinceName':provinceName,'cityCode':cityCode,'cityName':cityName,'regionCode':countyCode,'regionName':countyName,'districtCode':businessAreaCode,'districtName':businessAreaName}
        data.append(info)

    #聚合同一个行政区划的所有商圈
    for info in data:
        if json.dumps({'provinceCode':info['provinceCode'],'provinceName':info['provinceName'],'cityCode':info['cityCode'],'cityName':info['cityName'],'regionCode':info['regionCode'],'regionName':info['regionName']}) not in regionDict.keys():
            regionDict[json.dumps({'provinceCode':info['provinceCode'],'provinceName':info['provinceName'],'cityCode':info['cityCode'],'cityName':info['cityName'],'regionCode':info['regionCode'],'regionName':info['regionName']})] = [{'districtCode':info['districtCode'],'districtName':info['districtName']}]
        else:
            regionDict[json.dumps({'provinceCode':info['provinceCode'],'provinceName':info['provinceName'],'cityCode':info['cityCode'],'cityName':info['cityName'],'regionCode':info['regionCode'],'regionName':info['regionName']})].append({'districtCode':info['districtCode'],'districtName':info['districtName']})

    #聚合同一个市的所有行政区划
    for k,v in regionDict.items():
        k = json.loads(k)
        if json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName'],'cityCode':k['cityCode'],'cityName':k['cityName']}) not in cityDict.keys():
            cityDict[json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName'],'cityCode':k['cityCode'],'cityName':k['cityName']})] = [{'regionCode':k['regionCode'],'regionName':k['regionName'],'district':v}]
        else:
            cityDict[json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName'],'cityCode':k['cityCode'],'cityName':k['cityName']})].append({'regionCode':k['regionCode'],'regionName':k['regionName'],'district':v})

    #聚合城市
    for k,v in cityDict.items():
        k = json.loads(k)
        if json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName']}) not in provinceDict.keys():
            provinceDict[json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName']})] = [{'cityCode':k['cityCode'],'cityName':k['cityName'],'region':v}]
        else:
            provinceDict[json.dumps({'provinceCode':k['provinceCode'],'provinceName':k['provinceName']})].append({'cityCode':k['cityCode'],'cityName':k['cityName'],'region':v})

    #整理出最后结果
    for k,v in provinceDict.items():
        province = dict()
        k = json.loads(k)
        province['provinceCode'] = k['provinceCode']
        province['provinceName'] = k['provinceName']
        province['city'] = v
        provinceList.append(province)

    result = {'errorCode':200,'errorMsg':'success!','data':{'areaList':{'province':provinceList}}}
    return HttpResponse(json.dumps(result,ensure_ascii=False))


#查询业态字典
def queryBusinessTypeList(request):
    items = Dianping_cuisine.objects.all()

    businessTypeList = list()
    for item in items:
        businessTypeCode = item.cuisineCode
        businessTypeName = item.cuisineName.replace('\r','') #tbl_dianping_cuisine中存储的菜系名称都带了一个'\r'字符，此处处理掉

        info = {'businessTypeCode':businessTypeCode,'businessTypeName':businessTypeName}
        businessTypeList.append(info)

    result = {'errorCdoe':200,'errorMsg':'success!','data':{'businessTypeList':businessTypeList}}
    return HttpResponse(json.dumps(result,ensure_ascii=False))



#按不同级别地区查询，获取对应的店铺数量
def queryShopSum(request):

    #从请求中提取参数
    queryLevel = request.GET.get('queryLevel','')
    province = request.GET.get('province','')
    city = request.GET.get('city','')
    region = request.GET.get('region','')
    businessTypeCode = request.GET.get('businessTypeCode','')
    averageCostMin = request.GET.get('averageCostMin','')
    averageCostMax = request.GET.get('averageCostMax','')

    #检查参数是否有缺失
    if not queryLevel:
        error_msg = {'errorCode':'404','errorMsg':'缺少查询级别参数！！'}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))
    if not businessTypeCode:
        error_msg = {'errorCode': '404','errorMsg':'缺少业态参数！！'}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))
    elif not averageCostMin:
        error_msg = {'errorCode':'404','errorMsg':'缺少人均消费最低参数！！'}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))
    elif not averageCostMax:
        error_msg = {'errorCode': '404','errorMsg':'缺少人均消费最高参数！！'}
        return HttpResponse(json.dumps(error_msg,ensure_ascii=False))

    #将业态编码转换到对应的业态名称
    cuisineName = Dianping_cuisine.objects.filter(cuisineCode__icontains=businessTypeCode)[0].cuisineName
    cuisineName = cuisineName.replace('\r','')

    #返回结果格式
    shopInfoSum_list = list()
    result = {'errorCode':200,'errorMsg':'success!','data':{'shopInfoSum':shopInfoSum_list}}


    #queryLevel是country（全国）
    if queryLevel=='country':
        items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
        result['data']['shopInfoSum'].append({'province':'','city':'','region':'','district':'','shopCount':len(items),'mapLongitudeValue':'105.42857','mapLatitudeValue':'34.439187'})
        return HttpResponse(json.dumps(result))


    #queryLevel是province
    if queryLevel=='province':
        if province: #查询该省的 所有市 该业态 该消费区间 的 店铺数量排名
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('province').annotate(Count('province'))
            position = China_businessarea.objects.filter(provinceName__icontains=province)[0].provincePositionGCJ02
            result['data']['shopInfoSum'].append({'province':province,'city':'','region':'','district':'','shopCount':items[0][1],'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif not province: #省、市、区参数都为空，即默认查询全国数据
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('province').annotate(Count('province'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                province = item[0]
                shopCount = item[1]
                position = China_businessarea.objects.filter(provinceName__icontains=province)[0].provincePositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':'','region':'','district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))


    #queryLevel是city
    elif queryLevel=='city':
        if province and city: #当前查询级别为city，且省、市层级信息都存在
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('city').annotate(Count('city'))
            position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city)[0].cityPositionGCJ02
            result['data']['shopInfoSum'].append({'province':province,'city':city,'region':'','district':'','shopCount':items[0][1],'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif province and not city: #当前查询级别为city，但只选了省，表示查询该省所有市
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('city').annotate(Count('city'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                city = item[0]
                shopCount = item[1]
                position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city)[0].cityPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':'','district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif not province and not city: #省、市都空着，表示查询全国所有市的店铺数量
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('city').annotate(Count('city'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                city = item[0]
                shopCount = item[1]
                province = China_businessarea.objects.filter(cityName__icontains=city)[0].provinceName
                position = China_businessarea.objects.filter(cityName__icontains=city)[0].cityPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':'','district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

    #查询级别是行政区划
    elif queryLevel=='region':
        if province and city and region:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('adminRegion').annotate(Count('adminRegion'))
            position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city).filter(countyName__icontains=region)[0].countyPositionGCJ02
            result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':'','shopCount':items[0][1],'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif province and city and not region: #没有选region参数
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('adminRegion').annotate(Count('adminRegion'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                region = item[0]
                shopCount = item[1]
                position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city).filter(countyName__icontains=region)[0].countyPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif province and not city and not region: #没有选city、region参数
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('adminRegion').annotate(Count('adminRegion'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                region = item[0]
                shopCount = item[1]
                city = China_businessarea.objects.filter(provinceName__icontains=province).filter(countyName__icontains=region)[0].cityName
                position = China_businessarea.objects.filter(provinceName__icontains=province).filter(countyName__icontains=region)[0].countyPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif not province and not city and not region: #查询全国所有的行政区划符合该查询条件的店铺数量排名
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('adminRegion').annotate(Count('adminRegion'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                region = item[0]
                shopCount = item[1]
                #存在tbl_basic_shop_info表中行政区划名称与tbl_china_businessarea中不对应或不存在的情况，导致查询结果为空，按键取值时报错，捕获错误
                try:
                    city = China_businessarea.objects.filter(countyName__icontains=region)[0].cityName
                    province = China_businessarea.objects.filter(countyName__icontains=region)[0].provinceName
                    position = China_businessarea.objects.filter(countyName__icontains=region)[0].countyPositionGCJ02
                    result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':'','shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
                except Exception as e:
                    print('报错啦！！原因可能是tbl_basic_shop_info中查询到的行政区划名称在tbl_china_businessarea中不存在或名称不统一！！错误信息：%s，出错的位置：%s' % (str(e.args),item))
                    #将报错的行政区划名称写入文件
                    pass
            return HttpResponse(json.dumps(result))

    #查询级别是商圈
    elif queryLevel=='district': #接口设计定义里，没有传入district参数
        if province and city and region:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('businessArea').annotate(Count('businessArea'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                district = item[0]
                shopCount = item[1]
                position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city).filter(countyName__icontains=region).filter(businessAreaName__icontains=district)[0].businessAreaPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':district,'shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif province and city and not region: #没有选region参数
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('businessArea').annotate(Count('businessArea'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                district = item[0]
                shopCount = item[1]
                try:
                    region = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city).filter(businessAreaName__icontains=district)[0].countyName
                    position = China_businessarea.objects.filter(provinceName__icontains=province).filter(cityName__icontains=city).filter(businessAreaName__icontains=district)[0].businessAreaPositionGCJ02
                    result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':district,'shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
                except Exception as e:
                    #print('报错啦！！原因可能是tbl_basic_shop_info中查询到的行政区划名称在tbl_china_businessarea中不存在或名称不统一！！错误信息：%s，出错的位置：%s' % (str(e.args),item))
                    #将报错的商圈名称写入文件
                    pass
            return HttpResponse(json.dumps(result))

        elif province and not city and not region: #没有选city、region参数
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('businessArea').annotate(Count('businessArea'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                district = item[0]
                shopCount = item[1]
                region = China_businessarea.objects.filter(provinceName__icontains=province).filter(businessAreaName__icontains=district)[0].countyName
                city = China_businessarea.objects.filter(provinceName__icontains=province).filter(businessAreaName__icontains=district)[0].cityName
                position = China_businessarea.objects.filter(provinceName__icontains=province).filter(businessAreaName__icontains=district)[0].businessAreaPositionGCJ02
                result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':district,'shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
            return HttpResponse(json.dumps(result))

        elif not province and not city and not region:
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('businessArea').annotate(Count('businessArea'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            for item in items_sorted:
                district = item[0]
                shopCount = item[1]
                try:
                    region = China_businessarea.objects.filter(businessAreaName__icontains=district)[0].countyName
                    city = China_businessarea.objects.filter(businessAreaName__icontains=district)[0].cityName
                    province = China_businessarea.objects.filter(businessAreaName__icontains=district)[0].provinceName
                    position = China_businessarea.objects.filter(businessAreaName__icontains=district)[0].businessAreaPositionGCJ02
                    result['data']['shopInfoSum'].append({'province':province,'city':city,'region':region,'district':district,'shopCount':shopCount,'mapLongitudeValue':position.split(',')[1],'mapLatitudeValue':position.split(',')[0]})
                except Exception as e:
                    #print('报错啦！！原因可能是tbl_basic_shop_info中查询到的行政区划名称在tbl_china_businessarea中不存在或名称不统一！！错误信息：%s，出错的位置：%s' % (str(e.args),item))
                    #将报错的商圈名称写入文件
                    pass
            return HttpResponse(json.dumps(result))


#按商圈查询，获取店铺的详细信息
def queryShopDetail(request):

    #提取请求参数
    province = request.GET.get('province','')
    city = request.GET.get('city','')
    region = request.GET.get('region','')
    district = request.GET.get('district','')
    businessType = request.GET.get('businessType','')
    averageCostMin = request.GET.get('averageCostMin','')
    averageCostMax = request.GET.get('averageCostMax','')

    #检查参数
    errors = list()
    if not province:
        errors.append('缺少province参数！！')
    elif not city:
        errors.append('缺少city参数！！')
    elif not region:
        errors.append('缺少region参数！！')
    elif not district:
        errors.append('缺少district参数！！')
    elif not businessType:
        errors.append('缺少businessType参数！！')
    elif not averageCostMin:
        errors.append('缺少averageCostMin参数！！')
    elif not averageCostMax:
        errors.append('缺少averageCostMax参数！！')

    if errors: #如果缺少参数，返回错误提示信息
        result = {'errorCode':200,'errorMsg':errors}
        return HttpResponse(json.dumps(result))
    else:
        #将业态编码转换到对应的业态名称
        cuisineName = Dianping_cuisine.objects.filter(cuisineCode__icontains=businessType)[0].cuisineName
        cuisineName = cuisineName.replace('\r','')

        shopInfoList = list()
        result = {'errorCode':200,'errorMsg':'success!','data':{'shopInfoList':shopInfoList}}

        #从tbl_basic_shop_info中提取符合条件的信息
        items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(businessArea__icontains=district).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
        for item in items:
            shopInfo = dict()
            shopInfo['MdcShopID'] = item.MdcShopID #表中暂时无这个参数
            shopInfo['HuaLaLaShopID'] = item.HuaLaLaShopID #表中暂时无这个参数
            shopInfo['province'] = province
            shopInfo['city'] = city
            shopInfo['region'] = region
            shopInfo['district'] = district
            shopInfo['shopName'] = item.shopName
            shopInfo['averageCost'] = str(item.avgPrice)
            shopInfo['phone'] = item.telephone
            shopInfo['businessTime'] = item.businessTime
            shopInfo['address'] = item.address
            shopInfo['businessTypeCode'] = businessType
            shopInfo['businessTypeName'] = cuisineName
            if item.position:
                shopInfo['mapLongitudeValue'] = item.position.split(',')[0]
                shopInfo['mapLatitudeValue'] = item.position.split(',')[1]
            else:
                shopInfo['mapLongitudeValue'] = ''
                shopInfo['mapLatitudeValue'] = ''
            shopInfo['reviewLevel'] = item.starLevel #starLevel参数暂时tbl_basic_shop_info中没有
            shopInfoList.append(shopInfo)
        return HttpResponse(json.dumps(result))


#省/市/区按照业态分类的店铺数量
def queryBusinessTypeInfoList(request):

    #获取请求参数
    province = request.GET.get('province','')
    city = request.GET.get('city','')
    region = request.GET.get('region','')
    district = request.GET.get('district','')
    businessType = request.GET.get('businessType','')
    averageCostMin = request.GET.get('averageCostMin','')
    averageCostMax = request.GET.get('averageCostMax','')

    #检查参数
    errors = list()
    if not businessType:
        errors.append('缺少businessType参数！！')
    elif not averageCostMin:
        errors.append('缺少averageCostMin参数！！')
    elif not averageCostMax:
        errors.append('缺少averageCostMax参数！！')

    if errors: #如果缺少参数，返回错误提示信息
        result = {'errorCode':200,'errorMsg':errors}
        return HttpResponse(json.dumps(result))
    else: #从tbl_basic_shop_info中提取符合条件的信息
        #将业态代码转换到对应的业态名称
        cuisineName = Dianping_cuisine.objects.filter(cuisineCode__icontains=businessType)[0].cuisineName
        cuisineName = cuisineName.replace('\r','')

        businessTypeInfo = dict()
        result = {'errorCode':200,'errorMsg':'success!','data':{'businessTypeInfoList':[businessTypeInfo]}}

        #省市区商圈参数都存在
        if province and city and region and district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(businessArea__icontains=district).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
            shopCount = len(items)
            businessTypeInfo['province'] = province
            businessTypeInfo['city'] = city
            businessTypeInfo['region'] = region
            businessTypeInfo['district'] = district
            businessTypeInfo['businessTypeName'] = cuisineName
            businessTypeInfo['businessTypeCode'] = businessType
            businessTypeInfo['shopCount'] = shopCount
            return HttpResponse(json.dumps(result))

        #缺少商圈参数
        elif province and city and region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
            shopCount = len(items)
            businessTypeInfo['province'] = province
            businessTypeInfo['city'] = city
            businessTypeInfo['region'] = region
            businessTypeInfo['district'] = ''
            businessTypeInfo['businessTypeName'] = cuisineName
            businessTypeInfo['businessTypeCode'] = businessType
            businessTypeInfo['shopCount'] = shopCount
            return HttpResponse(json.dumps(result))

        #缺少行政区划、商圈参数
        elif province and city and not region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
            shopCount = len(items)
            businessTypeInfo['province'] = province
            businessTypeInfo['city'] = city
            businessTypeInfo['region'] = ''
            businessTypeInfo['district'] = ''
            businessTypeInfo['businessTypeName'] = cuisineName
            businessTypeInfo['businessTypeCode'] = businessType
            businessTypeInfo['shopCount'] = shopCount
            return HttpResponse(json.dumps(result))

        #缺少市、行政区划、商圈参数
        elif province and not city and not region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
            shopCount = len(items)
            businessTypeInfo['province'] = province
            businessTypeInfo['city'] = ''
            businessTypeInfo['region'] = ''
            businessTypeInfo['district'] = ''
            businessTypeInfo['businessTypeName'] = cuisineName
            businessTypeInfo['businessTypeCode'] = businessType
            businessTypeInfo['shopCount'] = shopCount
            return HttpResponse(json.dumps(result))

        #省、市、区、商圈参数全为空，默认查询全国
        elif not province and not city and not region and not district:
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax)
            shopCount = len(items)
            businessTypeInfo['province'] = ''
            businessTypeInfo['city'] = ''
            businessTypeInfo['region'] = ''
            businessTypeInfo['district'] = ''
            businessTypeInfo['businessTypeName'] = cuisineName
            businessTypeInfo['businessTypeCode'] = businessType
            businessTypeInfo['shopCount'] = shopCount
            return HttpResponse(json.dumps(result))


#品牌排名列表
def queryBrandList(request):

    #提取请求参数
    province = request.GET.get('province','')
    city = request.GET.get('city','')
    region = request.GET.get('region','')
    district = request.GET.get('district','')
    businessType = request.GET.get('businessType','')
    averageCostMin = request.GET.get('averageCostMin','')
    averageCostMax = request.GET.get('averageCostMax','')
    topNum = request.GET.get('topNum','')

    #检查参数
    errors = list()
    if not businessType:
        errors.append('缺少businessType参数！！')
    elif not averageCostMin:
        errors.append('缺少averageCostMin参数！！')
    elif not averageCostMax:
        errors.append('缺少averageCostMax参数！！')
    elif not topNum:
        errors.append('缺少topNum参数！！')

    if errors: #如果缺少参数，返回错误提示信息
        result = {'errorCode':200,'errorMsg':errors}
        return HttpResponse(json.dumps(result))
    else: #从tbl_basic_shop_info中提取符合条件的信息
        #将业态代码转换到对应的业态名称
        cuisineName = Dianping_cuisine.objects.filter(cuisineCode__icontains=businessType)[0].cuisineName
        cuisineName = cuisineName.replace('\r','')

        brandInfoList = list()
        result = {'errorCode':200,'errorMsg':'success!','data':{'brandInfoList':brandInfoList}}

        #省市区商圈参数都存在
        if province and city and region and district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(businessArea__icontains=district).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('brandName').annotate(Count('brandName'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            if not items:
                return HttpResponse(json.dumps(result))
            else:
                for item in items_sorted:
                    if not item[0]: #查询到的店铺都没有品牌，排除掉
                        return HttpResponse(json.dumps(result))
                    else:
                        brandInfo = dict()
                        #brandID = Basic_shop_info.objects.filter(brandName__icontains=item[0]).brandUrl.replace('http://www.dianping.com/brands/b','')
                        brandInfo['province'] = province
                        brandInfo['city'] = city
                        brandInfo['region'] = region
                        brandInfo['district'] = district
                        brandInfo['brandName'] = item[0]
                        #brandInfo['brandID'] = brandID #brandID暂时不存在于tbl_basic_shop_info中
                        brandInfo['shopCount'] = item[1]
                        brandInfoList.append(brandInfo)
                return HttpResponse(json.dumps(result))

        #缺少商圈参数
        elif province and city and region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(adminRegion__icontains=region).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('brandName').annotate(Count('brandName'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            if not items:
                return HttpResponse(json.dumps(result))
            else:
                for item in items_sorted:
                    if not item[0]: #查询到的店铺都没有品牌，排除掉
                        return HttpResponse(json.dumps(result))
                    else:
                        brandInfo = dict()
                        #brandID = Basic_shop_info.objects.filter(brandName__icontains=item[0]).brandUrl.replace('http://www.dianping.com/brands/b','')
                        brandInfo['province'] = province
                        brandInfo['city'] = city
                        brandInfo['region'] = region
                        brandInfo['district'] = ''
                        brandInfo['brandName'] = item[0]
                        #brandInfo['brandID'] = brandID #brandID暂时不存在于tbl_basic_shop_info中
                        brandInfo['shopCount'] = item[1]
                        brandInfoList.append(brandInfo)
                return HttpResponse(json.dumps(result))

        #缺少行政区划、商圈参数
        elif province and city and not region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(city__icontains=city).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('brandName').annotate(Count('brandName'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            if not items:
                return HttpResponse(json.dumps(result))
            else:
                for item in items_sorted:
                    if not item[0]: #查询到的店铺都没有品牌，排除掉
                        return HttpResponse(json.dumps(result))
                    else:
                        brandInfo = dict()
                        #brandID = Basic_shop_info.objects.filter(brandName__icontains=item[0]).brandUrl.replace('http://www.dianping.com/brands/b','')
                        brandInfo['province'] = province
                        brandInfo['city'] = city
                        brandInfo['region'] = ''
                        brandInfo['district'] = ''
                        brandInfo['brandName'] = item[0]
                        #brandInfo['brandID'] = brandID #brandID暂时不存在于tbl_basic_shop_info中
                        brandInfo['shopCount'] = item[1]
                        brandInfoList.append(brandInfo)
                return HttpResponse(json.dumps(result))

        #缺少市、行政区划、商圈参数
        elif province and not city and not region and not district:
            items = Basic_shop_info.objects.filter(province__icontains=province).filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('brandName').annotate(Count('brandName'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            if not items:
                return HttpResponse(json.dumps(result))
            else:
                for item in items_sorted:
                    if not item[0]: #查询到的店铺都没有品牌，排除掉
                        return HttpResponse(json.dumps(result))
                    else:
                        brandInfo = dict()
                        #brandID = Basic_shop_info.objects.filter(brandName__icontains=item[0]).brandUrl.replace('http://www.dianping.com/brands/b','')
                        brandInfo['province'] = province
                        brandInfo['city'] = ''
                        brandInfo['region'] = ''
                        brandInfo['district'] = ''
                        brandInfo['brandName'] = item[0]
                        #brandInfo['brandID'] = brandID #brandID暂时不存在于tbl_basic_shop_info中
                        brandInfo['shopCount'] = item[1]
                        brandInfoList.append(brandInfo)
                return HttpResponse(json.dumps(result))

        #省、市、区、商圈参数全为空，默认查询全国
        elif not province and city and not region and not district:
            items = Basic_shop_info.objects.filter(cuisine__icontains=cuisineName).filter(avgPrice__gte=averageCostMin).filter(avgPrice__lte=averageCostMax).values_list('brandName').annotate(Count('brandName'))
            items_sorted = sorted(items,key=lambda item:item[1],reverse=True)
            if not items:
                return HttpResponse(json.dumps(result))
            else:
                for item in items_sorted:
                    if not item[0]: #查询到的店铺都没有品牌，排除掉
                        return HttpResponse(json.dumps(result))
                    else:
                        brandInfo = dict()
                        #brandID = Basic_shop_info.objects.filter(brandName__icontains=item[0]).brandUrl.replace('http://www.dianping.com/brands/b','')
                        brandInfo['province'] = province
                        brandInfo['city'] = city
                        brandInfo['region'] = ''
                        brandInfo['district'] = ''
                        brandInfo['brandName'] = item[0]
                        #brandInfo['brandID'] = brandID #brandID暂时不存在于tbl_basic_shop_info中
                        brandInfo['shopCount'] = item[1]
                        brandInfoList.append(brandInfo)
                return HttpResponse(json.dumps(result))
