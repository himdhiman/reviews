from rest_framework import serializers
from main.models import TrackingList


class TrackingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingList
        fields = "__all__"
