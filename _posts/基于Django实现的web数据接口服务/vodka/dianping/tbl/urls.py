from django.conf.urls import url
from . import views
from . import companys


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^shop/summary/',views.summary,name='summary'),
    url(r'^shop/detail/',views.detail,name='detail'),
    url(r'^shop/feedback/$',views.feedback,name='feedback'),
    url(r'^shop/feedback/results/',views.results,name='results'),
    url(r'^shop/confirm/$',views.confirm,name='confirm'),
    url(r'^shop/confirm/results/',views.results,name='results'),
    url(r'^shop/queryShopSum/$',views.queryShopSum,name='queryShopSum'),
    url(r'^shop/queryShopDetail/$',views.queryShopSum,name='queryShopDetail'),
    url(r'^shop/queryBusinessTypeInfoList/$',views.queryBusinessTypeInfoList,name='queryBusinessTypeInfoList'),
    url(r'^shop/queryBrandList/$',views.queryBrandList,name='queryBrandList'),
    url(r'^shop/queryBusinessTypeList/$',views.queryBusinessTypeList,name='queryBusinessTypeList'),
    url(r'^shop/queryAreaList/$',views.queryAreaList,name='queryAreaList'),
]

