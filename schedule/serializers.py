from rest_framework import serializers

from .models import *


class EmailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailList
        fields = ['email', 'dispatch_date']


class ScheduleSerializer(serializers.Serializer):

    contacts = EmailListSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ['contacts']

    def create(self, initial_data):
        import pdb; pdb.set_trace()

        # modify initial data to validated
        contacts = initial_data['contacts']
        days_to_skip = initial_data['days_to_skip']

        dispatcher = AssesEmailDates(emails=contacts, skip_dates=days_to_skip)
        dispatches = dispatcher.assesing_datetime()


        validated_data = {'contacts': []}

        for email in dispatches:
            validated_data['contacts'].append(
                {'email': email,
                 'dispatch_date': email['email']
                 }
            )


        schedule = Schedule.objects.create()

        for email in validated_data['contacts']:
            email = EmailList.objects.create(
                email=email['email'],
                dispatch_date=email['dispatch_date']
            )
            schedule.contacts.add(email)

        return schedule
