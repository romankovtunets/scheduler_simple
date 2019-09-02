from django.db import models


class EmailList(models.Model):
    email = models.EmailField()
    dispatch_date = models.DateTimeField(
        blank=True,
    )


class Schedule(models.Model):
    contacts = models.ManyToManyField(EmailList)