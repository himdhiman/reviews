from django.conf import settings
from main.models import Product, TrackingList


class FilterData:
    @staticmethod
    def filter_data(data):
        filtered_data = {}
        filtered_data["name"] = data["data"]["customer"]["traits"]["name"]
        filtered_data["phone_number"] = (
            data["data"]["customer"]["country_code"]
            + data["data"]["customer"]["phone_number"]
        )
        filtered_data["order_id"] = data["data"]["customer"]["traits"]["last_order_id"]
        filtered_data["product_id"] = data["data"]["customer"]["traits"][
            "last_order_name"
        ]
        filtered_data["mail_id"] = data["data"]["customer"]["traits"]["Email Id"]
        return data["data"]["message"]["message"], filtered_data


class IsInTrackingList:
    @staticmethod
    def is_in_tracking_list(data):
        if TrackingList.objects.filter(phone_number=data).exists():
            return True
        else:
            return False


class GetPushData:
    @staticmethod
    def get_push_data(context, data):
        required_data = []
        for row in data:
            if row[0] == context["product_id"]:
                required_data = row
                break
        if len(required_data) == 0:
            print("No Data Found")
            return
        required_data[-1] = [i.strip() for i in required_data[-1].split("\n") if i]
        product_list = []
        variant_list = []
        push_data = []
        for i in required_data[-1]:
            qs = Product.objects.filter(sku_number=i)
            if len(qs) != 0:
                product_list.append(qs[0].product_name)
                variant_list.append(qs[0].variant_id)
        for i in range(len(product_list)):
            push_data.append(
                [
                    context["first_message"],
                    context["second_message"],
                    5,
                    "",
                    context["name"],
                    context["mail_id"],
                    str(variant_list[i]),
                    product_list[i],
                ]
            )
    
        return push_data


class PushData:
    @staticmethod
    def push_data(data):
        SHEET_REVIEWS = settings.GOOGLE_SHEETS_CLIENT.open(settings.REVIEW_SHEET_NAME)
        sheet_instance = SHEET_REVIEWS.get_worksheet(0)
        sheet_instance.append_rows(data)
        return
