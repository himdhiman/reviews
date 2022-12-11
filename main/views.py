from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from main.helpers import FilterData, IsInTrackingList
from main.models import TrackingList
from main.serializers import TrackingListSerializer
from main import tasks

# from main.spreadsheet import get_data


class DefaultView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        request_data = request.data

        if request_data["type"] != "message_received":
            return Response(status=status.HTTP_200_OK)

        phone_number = (
            request_data["data"]["customer"]["country_code"]
            + request_data["data"]["customer"]["phone_number"]
        )

        if IsInTrackingList.is_in_tracking_list(phone_number):
            message = request_data["data"]["message"]["message"]
            query_object = TrackingList.objects.get(phone_number=phone_number)
            if not query_object.first_message:
                query_object.first_message = message
                query_object.save()
            elif not query_object.second_message:
                query_object.second_message = message
                query_object.save()
            else:
                data = TrackingListSerializer(query_object).data
                query_object.delete()
                tasks.populateReview.delay(data)
            return Response(status=status.HTTP_200_OK)

        
        message, filtered_data = FilterData.filter_data(request_data)

        if message == settings.TRACKING_MESSAGE:
            print(filtered_data)
            TrackingList.objects.create(**filtered_data)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
