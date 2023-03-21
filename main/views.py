from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import re

from main.helpers import FilterData, IsInTrackingList
from main.models import TrackingList


class DefaultView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        request_data = request.data
        print(request_data)
        if request_data["type"] == "message_api_delivered" or request_data["type"] == "message_api_failed":
            req = requests.post(settings.THIRD_PARTY_URL, json=request_data, headers={
                "Content-Type": "application/json",
            })
            return Response(status=status.HTTP_200_OK)

        if request_data["type"] == "message_received":
            phone_number = (
                request_data["data"]["customer"]["country_code"]
                + request_data["data"]["customer"]["phone_number"]
            )
            message = request_data["data"]["message"]["message"]
            if message == "":
                Response(status=status.HTTP_200_OK)

            regex_expression = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
            regex_processor = re.compile(regex_expression);
            regex_matcher = re.match(regex_processor, message)

            if message == settings.EZIFY_MESSAGE or regex_matcher is not None:
                req = requests.post(settings.EZIFY_URL, json=request_data, headers={
                    "Content-Type": "application/json",
                })
                print(req)
           
            if IsInTrackingList.is_in_tracking_list(phone_number):
                query_object = TrackingList.objects.get(phone_number=phone_number)
                if not query_object.first_message:
                    query_object.first_message = message
                    query_object.save()
                elif not query_object.second_message:
                    query_object.second_message = message
                    query_object.save()
                return Response(status=status.HTTP_200_OK)

            message, filtered_data = FilterData.filter_data(request_data)

            if message == settings.TRACKING_MESSAGE:
                TrackingList.objects.create(**filtered_data)
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_200_OK)
