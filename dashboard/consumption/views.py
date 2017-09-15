# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate

from models import UserData, ConsumptionData

from graphos.sources.model import SimpleDataSource
from graphos.renderers.gchart import LineChart, AreaChart

def mainpage(request):
    options = {'summary': 'Summary View', 'detail': 'Detail View'}
    context = {'options' : options.items()}
    return render(request, 'consumption/main.html', context)

# Function to calculate average and total consumption
def aggregate_consumption():
    # Average and total consumption of all users in a day
    consumption = ConsumptionData.objects.annotate(d=TruncDate('dateinfo')).values('d').annotate(agg=Avg('consumption'), tot=Sum('consumption'))

    distinct_dates = [each['d'] for each in consumption]
    avg_consumption = [each['agg'] for each in consumption]
    tot_consumption = [each['tot'] for each in consumption]
    return distinct_dates, avg_consumption, tot_consumption

def summary(request):
    xdata, avgdata, totdata = aggregate_consumption()

    # AreaChart for average consumption
    data = [['Date', 'Average consumption']] + [[x, av] for x, av in zip(xdata, avgdata)]
    avgchart = AreaChart(SimpleDataSource(data=data), options={'title': \
                      'Average Energy Consumption of All Users from %s to %s' \
                      %(xdata[0], xdata[-1]), 'legend': {'position': 'top'}, \
                      'vAxes': {0: {'title': 'Average energy consumption (Wh)'}},\
                      'hAxes': {0: {'title': 'Date energy consumption data collected'}}})

    # LineChart for total consumption
    data = [['Date', 'Total consumption']] + [[x, tot] for x, tot in zip(xdata, totdata)]
    totchart = LineChart(SimpleDataSource(data=data), options={'title': \
                      'Total Energy Consumption of All Users from %s to %s' \
                      %(xdata[0], xdata[-1]), 'legend': {'position': 'top'}, \
                      'vAxes': {0: {'title': 'Total energy consumption (Wh)'}}, \
                      'hAxes': {0: {'title': 'Date energy consumption data collected'}},\
                      'colors': ['green']})

    # Data for user data table
    users = UserData.objects.all()

    context = {'avgchart': avgchart, 'totchart': totchart, 'users': users}
    return render(request, 'consumption/summary.html', context)

def detail(request):
    users = UserData.objects.values_list('userid', flat=True)
    context = { 'users': users, }
    return render(request, 'consumption/detail.html', context)

def user_detail(request, uid):
    user = UserData.objects.get(userid=uid)
    cdata = ConsumptionData.objects.filter(user=uid).annotate(d=TruncDate('dateinfo')).values('d').annotate(agg=Avg('consumption'))
    xdata = [each['d'] for each in cdata]
    avgdata = [each['agg'] for each in cdata]

    # LineChart for average consumption
    data = [['Date', 'Average consumption']] + [[x, av] for x, av in zip(xdata, avgdata)]
    avgchart = LineChart(SimpleDataSource(data=data), options={'title': \
                      'Average Energy Consumption of User %d from %s to %s' \
                      %(int(uid), xdata[0], xdata[-1]), 'legend': {'position': 'top'}, \
                      'vAxes': {0: {'title': 'Average energy consumption (Wh)'}},\
                      'hAxes': {0: {'title': 'Date energy consumption data collected'}}})

    context = {'user': user, 'avgchart': avgchart}
    return render(request, 'consumption/userdetail.html', context)
