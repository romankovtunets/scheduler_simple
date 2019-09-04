from django.core.validators import EmailValidator
from rest_framework import serializers
from datetime import datetime

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


    def validate(self, data):
        """ Validate incoming data
        """
        # check if date error present
        if 'invalid date' in data:
            raise serializers.ValidationError(data['invalid date'])

        # validate email
        email_validator = EmailValidator()
        for contact in data['contacts']:
            try:
                email_validator(contact['email'])
            except ValueError:
                raise serializers.ValidationError(
                    'Email address is not valid'
                )

        return data


    def to_internal_value(self, data):
        """ Modify initial data to validated
        """

        contacts = data['contacts']
        skip_days = data['days_to_skip']

        # validate date format and pass errors if invalid
        iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        errors = {}

        for date in skip_days:
            try:
                assert datetime.strptime(date, iso_format)
            except ValueError:
                errors['invalid date'] = \
                    "Dates are not in ISO format"


        if not errors:
            dispatcher = AssesEmailDates(emails=contacts, skip_dates=skip_days)
            dispatches = dispatcher.assesing_datetime()

            validated_data = {'contacts': []}

            for email in dispatches:
                validated_data['contacts'].append(
                    {'email': email,
                     'dispatch_date': dispatches[email],
                     }
                )
        else:
            validated_data = errors

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
