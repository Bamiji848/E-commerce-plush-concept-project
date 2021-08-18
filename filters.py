from django.contrib.auth.models import User
from plush_app.models import ShopProduct
import django_filters


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = ShopProduct
        fields = ['product_price1']
