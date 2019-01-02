from django.db import models


class Basic_shop_info(models.Model):
    shopID = models.CharField(max_length=20,primary_key=True)
    shopName = models.CharField(max_length=200,default='')
    shopLogo = models.CharField(max_length=1000,default='')
    province = models.CharField(max_length=20,default='')
    city = models.CharField(max_length=100,default='')
    adminRegion = models.CharField(max_length=100,default='')
    businessArea = models.CharField(max_length=100,default='')
    address = models.CharField(max_length=200,default='')
    position = models.CharField(max_length=100,default='')
    mapAddr = models.CharField(max_length=200,default='')
    telephone = models.CharField(max_length=100,default='')
    businessTime = models.CharField(max_length=200,default='')
    avgPrice = models.DecimalField(max_digits=10,decimal_places=1,default='0')
    isHllShop = models.CharField(max_length=20,default='')
    hllShopID = models.CharField(max_length=20,default='')
    hllShopName = models.CharField(max_length=200,default='')
    relCompany = models.CharField(max_length=200,default='')
    createStamp = models.CharField(max_length=200,default='')
    actionStamp = models.CharField(max_length=200,default='')
