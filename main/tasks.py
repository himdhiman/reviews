from datetime import datetime
from celery import shared_task
from django.conf import settings
from main.helpers import GetPushData, PushData
from main.models import Product, TrackingList
from main.serializers import TrackingListSerializer
from dateutil.tz import gettz


@shared_task(bind=True)
def syncProductIdAndName(self):
    SHEET_ORDERS = settings.GOOGLE_SHEETS_CLIENT.open(settings.ORDER_SHEET_NAME)
    sheet_instance = SHEET_ORDERS.get_worksheet(1)
    data = sheet_instance.get_values("A:C")
    for row in data:
        query_set = Product.objects.filter(sku_number=row[0])
        if len(query_set) == 0:
            product = Product(sku_number=row[0], product_name=row[1], variant_id=row[2])
            product.save()
        else:
            if query_set[0].product_name != row[1]:
                query_set[0].product_name = row[1]
                query_set[0].save()
            if query_set[0].variant_id != row[2]:
                query_set[0].variant_id = row[2]
                query_set[0].save()
    pass


@shared_task(bind=True)
def cleanReviews(self):
    print("Clean Reviews Called")
    SHEET_ORDERS = settings.GOOGLE_SHEETS_CLIENT.open(settings.ORDER_SHEET_NAME)
    sheet_instance = SHEET_ORDERS.get_worksheet(0)
    data = sheet_instance.get_values("A:D")
    qs = TrackingList.objects.all()
    curr_time = datetime.now()
    for i in qs:
        utc_time = i.created_at
        ist_time = utc_time.astimezone(gettz(settings.TIME_ZONE)).replace(tzinfo=None)
        if (
            (curr_time - ist_time).seconds
        ) / 3600 >= settings.TRACKINGLIST_CLEANUP_INTERVAL:
            context = TrackingListSerializer(i).data
            push_data = GetPushData.get_push_data(context, data)
            PushData.push_data(push_data)
            i.delete()
    pass
