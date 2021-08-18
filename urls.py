
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from plush_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from plush_app.sitemaps import Static_Sitemap
from plush_app.models import ShopProduct

sitemaps = {
    'shop': GenericSitemap({
        'queryset': ShopProduct.objects.all()
    }, priority=0.9),
    'static': Static_Sitemap,
}


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('payteuiosth/', views.payteuiosth, name='payteuiosth'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('register/', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('gallery/', views.gallery, name='gallery'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^sitemap\.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('admin/', admin.site.urls),
    path('admin/order/<int:order_id>/', views.admin_order_detail,name='admin_order_detail'),
    # path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),
    path(r'captcha/', include('captcha.urls')),
    path('searchposts/', views.searchposts, name='searchposts'),
    path('searchfilter/', views.searchfilter, name='searchfilter'),
    path('plush_app', include('plush_app.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
