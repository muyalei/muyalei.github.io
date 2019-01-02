#/usr/bin/python 
# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from . models import Basic_shop_info
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
