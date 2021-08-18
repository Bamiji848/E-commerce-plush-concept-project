from django.contrib import admin
from plush_app.models import Category,Login,OrderItem,Order, ShopProduct,FontawesomeDesc, Contact, FontawesomeDesc2, FontawesomeDesc3, FlashSale, MeetUs,Media,Carosue

admin.site.site_header = 'Plush Online Store'

admin.site.register(FontawesomeDesc)
admin.site.register(FontawesomeDesc2)
admin.site.register(FontawesomeDesc3)
admin.site.register(FlashSale)
admin.site.register(MeetUs)
admin.site.register(Contact)
admin.site.register(Login)
admin.site.register(Carosue)
admin.site.register(Media)

import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'

# def order_pdf(obj):
#     return mark_safe('<a href="{}">PDF</a>'.format(
#         reverse('admin_order_pdf', args=[obj.id])))
# order_pdf.short_description = 'Invoice'

from django.urls import reverse
from django.utils.safestring import mark_safe
def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('admin_order_detail', args=[obj.id])))

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
                    'updated',order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['product_name1', 'slug', 'product_price1', 'available']
    list_filter = ['available']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('product_name1',)}


admin.site.register(ShopProduct, ShopProductAdmin)
