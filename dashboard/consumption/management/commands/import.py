
import os
import csv
import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone

from dashboard.settings import DATA_PATH
from consumption.models import UserData, ConsumptionData

class Command(BaseCommand):
    help = 'import data'

    def _populate_userdata(self, filepath):
        with open(filepath) as inp:
            reader = csv.reader(inp, delimiter=',')
            objs = [UserData(userid=row[0], area=row[1], tariff=row[2]) \
                    for row in reader if row[0][0] != 'i']
            UserData.objects.bulk_create(objs)

    def _populate_consumptiondata(self, dirpath):
        for filename in os.listdir(dirpath):
            # User id of consumption data is the name of the file
            # Remove the file extention to get the userid i.e. uid
            uid = filename.split('.')[0]
            filename = os.path.join(dirpath, filename)
            # To avoid naive datetime
            tz = get_current_timezone()
            with open(filename) as inp:
                reader = csv.reader(inp, delimiter=',')
                objs = []
                for row in reader:
                    if row[0][0] == 'd': continue
                    # Convert to datetime object
                    datefield = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    # Making datefield timezone aware
                    datefield = tz.localize(datefield)
                    objs.append(ConsumptionData(dateinfo=datefield, consumption=row[1],\
                                user=UserData.objects.get(userid=uid)))
                ConsumptionData.objects.bulk_create(objs)

    def handle(self, *args, **options):
        filepath = os.path.join(DATA_PATH, 'user_data.csv')
        self._populate_userdata(filepath)

        dirpath = os.path.join(DATA_PATH, 'consumption')
        self._populate_consumptiondata(dirpath)
