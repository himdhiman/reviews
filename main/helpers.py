from main.models import TrackingList


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
