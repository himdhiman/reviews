import json
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from main.spreadsheet import get_data

# Create your views here.


class DefaultView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        get_data()
        
  

        return Response(status=status.HTTP_200_OK)
