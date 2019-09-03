from rest_framework import serializers

from .models import *
from .logic import AssesEmailDates


class EmailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailList
        fields = ['email', 'dispatch_date']


class ScheduleSerializer(serializers.Serializer):

    contacts = EmailListSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ['contacts']

    # validators


    def to_internal_value(self, data):

        # modify initial data to validated
        contacts = data['contacts']
        days_to_skip = data['days_to_skip']

        dispatcher = AssesEmailDates(emails=contacts, skip_dates=days_to_skip)
        dispatches = dispatcher.assesing_datetime()


        validated_data = {'contacts': []}

        for email in dispatches:
            validated_data['contacts'].append(
                {'email': email,
                 'dispatch_date': dispatches[email],
                 }
            )

        return validated_data

    def create(self, validated_data):

        schedule = Schedule.objects.create()

        for contact in validated_data['contacts']:
            email = EmailList.objects.create(
                email=contact['email'],
                dispatch_date=contact['dispatch_date']
            )
            schedule.contacts.add(email)

        return schedule
