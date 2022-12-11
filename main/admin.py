from django.contrib import admin
from main import models


class CustomTrackingListAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "created_at", "mail_id")


admin.site.register(models.TrackingList)
