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
    url(r'^company/summary/',companys.summary,name='summary'),
    url(r'^company/detail/',companys.detail,name='detail')
]

