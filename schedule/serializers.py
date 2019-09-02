from rest_framework import serializers
from rest_framework.parsers import JSONParser

from .models import *


class EmailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailList
        fields = '__all__'


class ScheduleSerializer(serializers.Serializer):

    contacts = EmailListSerializer(many=True)

