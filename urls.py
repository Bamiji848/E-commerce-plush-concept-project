from django.conf.urls import url
from . import views
from .views import (searchposts)
from .views import (searchfilter)

app_name = 'plush_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.register, name='register'),
    url(r'^$', searchposts, name='searchposts'),
    url(r'^search/$', views.searchfilter, name='searchfilter'),
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^order_create/$', views.order_create, name='order_create'),
    url(r'^shop/(?P<category_slug>[-\w]+)/$', views.shop, name='product_list_by_category'),
    url(r'^shop_single(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.shop_single, name='shop_single'),
]

