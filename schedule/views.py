from rest_framework import generics
from rest_framework.decorators import api_view
import datetime

from .serializers import *
from .models import *
from .logic import AssesEmailDates


class ScheduleList(generics.ListAPIView):

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    class Meta:
        fields = '__all__'


@api_view(['POST'])
def schedule_create(request):

    data = request.data
    contacts = data['contacts']
    days_to_skip = data['days_to_skip']
    dispatcher = AssesEmailDates(emails=contacts, skip_dates=days_to_skip)
    dispatches = dispatcher.assesing_datetime()

    schedule = Schedule.objects.create()

    for email in dispatches:
        email = EmailList.objects.create(
            email=email,
            dispatch_date=dispatches[email]
        )
        schedule.contacts.add(email)

    return schedule.save()

