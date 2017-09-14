# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserData(models.Model):
    userid = models.IntegerField(primary_key=True, unique=True)
    area = models.CharField(max_length=150)
    tariff = models.CharField(max_length=150)

class ConsumptionData(models.Model):
    dateinfo = models.DateTimeField()
    consumption = models.FloatField()
    user = models.ForeignKey(UserData, to_field='userid', on_delete=models.CASCADE)
