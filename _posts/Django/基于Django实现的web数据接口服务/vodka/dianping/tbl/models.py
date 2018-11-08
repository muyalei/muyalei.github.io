from django.db import models
import time



class Basic_shop_info(models.Model):
    shopID = models.SmallIntegerField(primary_key=True)
    shopName = models.CharField(max_length=100,default='')
    shopLogo = models.CharField(max_length=1000,default='')
    brandName = models.CharField(max_length=50,default='')
    cuisine = models.CharField(max_length=50,default='')
    cuisineAlias = models.CharField(max_length=50,default='')
    province = models.CharField(max_length=50,default='')
    city = models.CharField(max_length=100,default='')
    adminRegion = models.CharField(max_length=100,default='')
    businessArea = models.CharField(max_length=100,default='')
    address = models.CharField(max_length=200,default='')
    position = models.CharField(max_length=100,default='')
    mapAddr = models.CharField(max_length=200,default='')
    telephone = models.CharField(max_length=100,default='')
    businessTime = models.CharField(max_length=200,default='')
    avgPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    isHllShop = models.SmallIntegerField(default=0)
    hllShopID = models.SmallIntegerField(default=0)
    hllShopName = models.CharField(max_length=50,default='')
    relCompany = models.CharField(max_length=100,default='')
    createStamp = models.DateField(default=time.strftime('%Y-%m-%d',time.localtime()))
    actionStamp = models.DateField(auto_now=True)


class Dianping_cuisine(models.Model):
    itemID = models.SmallIntegerField(primary_key=True)
    cuisineCode = models.CharField(max_length=4,default='0000')
    cuisineName = models.CharField(max_length=50,default='')
    cuisineDesc = models.CharField(max_length=1000,default='')
    createStamp = models.DateField(default=time.strftime('%Y-%m-%d', time.localtime()))
    actionStamp = models.DateField(auto_now=True)


class China_businessarea(models.Model):
    provinceName = models.CharField(max_length=50,default='')
    provinceCode = models.CharField(max_length=6,default='')
    provincePositionGCJ02 = models.CharField(max_length=50,default='')
    provincePositionBD09 = models.CharField(max_length=50,default='')
    cityName = models.CharField(max_length=50,default='')
    cityCode = models.CharField(max_length=6,default='')
    cityPositionGCJ02 = models.CharField(max_length=50,default='')
    cityPositionBD09 = models.CharField(max_length=50,default='')
    countyName = models.CharField(max_length=50,default='')
    countyCode = models.CharField(max_length=6,default='')
    countyPositionGCJ02 = models.CharField(max_length=50,default='')
    countyPositionBD09 = models.CharField(max_length=50,default='')
    businessAreaName = models.CharField(max_length=50,default='')
    businessAreaPositionGCJ02 = models.CharField(max_length=50,default='')
    businessAreaPositionBD09 = models.CharField(max_length=50,default='')




