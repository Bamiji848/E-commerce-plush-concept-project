from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import reverse
from decimal import Decimal
from django.db.models import F, Sum
# from django.db.models.functions import Sum

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plush_app:product_list_by_category', args=[self.slug])


class FontawesomeDesc(models.Model):
    fd_title = models.CharField(
        max_length=50, verbose_name='font awesome description title')
    fd_description = models.CharField(
        max_length=200, verbose_name='font awesome description')

    def __str__(self):
        return self.fd_title


class FontawesomeDesc2(models.Model):
    fd_title2 = models.CharField(
        max_length=50, verbose_name='font awesome description title')
    fd_description2 = models.CharField(
        max_length=200, verbose_name='font awesome description')

    def __str__(self):
        return self.fd_title2


class FontawesomeDesc3(models.Model):
    fd_title3 = models.CharField(
        max_length=50, verbose_name='font awesome description title')
    fd_description3 = models.CharField(
        max_length=200, verbose_name='font awesome description')

    def __str__(self):
        return self.fd_title3


class FlashSale(models.Model):
    flashsale_title = models.CharField(
        max_length=100, verbose_name='flashsale title')
    flashsale_description = models.CharField(
        max_length=300, verbose_name='flashsale description')
    flashsale_date = models.DateField()
    flashsale_img = models.ImageField(
        null=True, blank=True, upload_to='images', verbose_name='Post product image5')

    def __str__(self):
        return self.flashsale_title


class MeetUs(models.Model):
    meet_details = models.CharField(
        max_length=500, verbose_name='meet_details')
    meet_img = models.ImageField(
        null=True, blank=True, upload_to='images', verbose_name='meet us image')

    def __str__(self):
        return self.meet_details


class Testimonials(models.Model):
    testimonial_detail = models.CharField(
        max_length=100, verbose_name='testimonial detail')
    testimonial_detail2 = models.CharField(
        max_length=100, verbose_name='testimonial detail')
    testimonial_detail3 = models.CharField(
        max_length=100, verbose_name='testimonial detail')
    testimonial_detail4 = models.CharField(
        max_length=100, verbose_name='testimonial detail')
    testimonial_name = models.CharField(
        max_length=100, verbose_name='testimonial name')
    testimonial_name2 = models.CharField(
        max_length=100, verbose_name='testimonial name')
    testimonial_name3 = models.CharField(
        max_length=100, verbose_name='testimonial name')
    testimonial_name4 = models.CharField(
        max_length=100, verbose_name='testimonial name')
    testimonial_job = models.CharField(
        max_length=100, verbose_name='testimonial job')
    testimonial_job2 = models.CharField(
        max_length=100, verbose_name='testimonial job')
    testimonial_job3 = models.CharField(
        max_length=100, verbose_name='testimonial job')
    testimonial_job4 = models.CharField(
        max_length=100, verbose_name='testimonial job')

    def __str__(self):
        return self.testimonial_detail


class Contact(models.Model):
    name = models.CharField(max_length=100)
    # subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    category = models.ForeignKey(Category, related_name='shopproduct', on_delete=models.CASCADE)
    product_name1 = models.CharField(max_length=100, verbose_name='product1')
    product_content = models.CharField(max_length=500, verbose_name='content')
    product_img1 = models.ImageField(upload_to='images', verbose_name='product1 image')
    product_desc1 = models.CharField(max_length=100, verbose_name='product1_desc')
    product_price1 = models.FloatField()
    slug = models.SlugField(max_length=1000, db_index=True)
    available = models.BooleanField(default=True)
    


    class Meta:
        ordering = ('product_name1', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.product_name1

    def get_absolute_url(self):
        return reverse('plush_app:shop_single', args=[self.id, self.slug])

class Login(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=8, verbose_name='password')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("plush_app:shop", kwargs={'slug': self.slug})

    def get_addtocart_url(self):
        return reverse('plush_app:cart_message', kwargs={'slug': self.slug})


class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    mobile_number = models.PositiveIntegerField()
    alternative_number = models.PositiveIntegerField()


    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_price1 = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.product.product_price1 * self.quantity

class Media(models.Model):
    name = models.CharField(max_length=100)
    media = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.name
        
class Carosue(models.Model):
    heading = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='images', verbose_name='carosue image')

    def __str__(self):
        return self.heading
