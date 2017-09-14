# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.test import TestCase
from django.db.models import Avg, Sum
from django.utils.timezone import get_current_timezone

from models import UserData, ConsumptionData
from views import aggregate_consumption

def create_data(uid, area, tariff, date1, date2, cons1, cons2):
    tz = get_current_timezone()
    UserData.objects.create(userid=uid, area=area, tariff=tariff)
    d1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    d1 = tz.localize(d1)
    d2 = datetime.datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    d2 = tz.localize(d2)
    ConsumptionData.objects.create(dateinfo=d1, consumption=cons1, \
                                   user=UserData.objects.get(userid=uid))
    ConsumptionData.objects.create(dateinfo=d2, consumption=cons2, \
                                   user=UserData.objects.get(userid=uid))

# Testing models
class UserDataTestCase(TestCase):
    def setUp(self):
        UserData.objects.create(userid=100, area='a10', tariff='t10')
        UserData.objects.create(userid=120, area='a10', tariff='t11')

    def test_usertariff(self):
        u1 = UserData.objects.get(userid=120)
        u2 = UserData.objects.get(userid=100)
        self.assertEqual(u1.tariff, 't11')
        self.assertEqual(u2.tariff, 't10')

class ConsumptionDataTestCase(TestCase):
    def setUp(self):
        create_data(14, 'a1', 't0', '2017-09-14 07:00:00', '2017-09-14 07:30:00', \
                    89.0, 150.0)

    def test_consumption(self):
        c = ConsumptionData.objects.filter(user=14)
        self.assertEqual(c[0].consumption, 89.0)
        self.assertEqual(c[1].dateinfo.date(), datetime.datetime(2017, 9, 14).date())
        self.assertEqual(c[1].consumption, 150.0)

# Testing views.aggregate_consumption()
class TestAggregateConsumption(TestCase):
    def setUp(self):
        create_data(1, 'a1', 't0', '2017-09-14 07:00:00', '2017-09-15 07:30:00', \
                    89.0, 150.0)
        create_data(2, 'a2', 't1', '2017-09-14 08:00:00', '2017-09-15 07:00:00', \
                    189.0, 50.0)

    def test_aggregateconsumption(self):
        dateinfo, avg, tot = aggregate_consumption()
        ans = ([datetime.date(2017, 9, 14), datetime.date(2017, 9, 15)], \
                [139.0, 100.0], [278.0, 200.0])
        self.assertEqual((dateinfo, avg, tot), ans)
