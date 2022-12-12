from django.contrib import admin
from main import models


class TrackingListAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "created_at", "mail_id")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku_number", "product_name", "variant_id")


admin.site.register(models.TrackingList, TrackingListAdmin)
admin.site.register(models.Product, ProductAdmin)
