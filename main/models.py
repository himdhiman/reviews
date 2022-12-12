from django.db import models


class TrackingList(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=40)
    product_id = models.CharField(max_length=40)
    mail_id = models.EmailField(max_length=254, null=True, blank=True)
    first_message = models.TextField(null=True, blank=True)
    second_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name + " | " + self.phone_number


class Product(models.Model):
    sku_number = models.CharField(max_length=40)
    product_name = models.CharField(max_length=256)
    variant_id = models.CharField(max_length=256)

    def __str__(self):
        return self.sku_number + " | " + self.product_name
