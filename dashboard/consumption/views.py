# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Avg, Sum

from models import UserData, ConsumptionData

from graphos.sources.model import SimpleDataSource
from graphos.renderers.gchart import LineChart, AreaChart

# Function to calculate average and total consumption
def aggregate_consumption():
    distinct_dates = sorted(set(each[0].date() for each in ConsumptionData.objects.values_list('dateinfo').distinct()))

    # Average and total consumption of all users in a day
    consumption = [ConsumptionData.objects.filter(dateinfo__startswith=each).aggregate(agg=Avg('consumption'), tot=Sum('consumption')) for each in distinct_dates]
    avg_consumption = [each['agg'] for each in consumption]
    tot_consumption = [each['tot'] for each in consumption]

    return list(distinct_dates), avg_consumption, tot_consumption

def summary(request):
    xdata, avgdata, totdata = aggregate_consumption()

    # LineChart for average consumption
    data = [['Date', 'Average consumption']] + [[x, av] for x, av in zip(xdata, avgdata)]
    avgchart = LineChart(SimpleDataSource(data=data), options={'title': \
                      'Average Energy Consumption of All Users from %s to %s' \
                      %(xdata[0], xdata[-1]), 'legend': {'position': 'top'}, \
                      'vAxes': {0: {'title': 'Average energy consumption (Wh)'}},\
                      'hAxes': {0: {'title': 'Date energy consumption data collected'}}})

    # AreaChart for total consumption
    data = [['Date', 'Total consumption']] + [[x, tot] for x, tot in zip(xdata, totdata)]
    totchart = AreaChart(SimpleDataSource(data=data), options={'title': \
                      'Total Energy Consumption of All Users from %s to %s' \
                      %(xdata[0], xdata[-1]), 'legend': {'position': 'top'}, \
                      'vAxes': {0: {'title': 'Total energy consumption (Wh)'}}, \
                      'hAxes': {0: {'title': 'Date energy consumption data collected'}},\
                      'colors': ['green']})

    # Data for user data table
    users = UserData.objects.order_by('userid')

    context = {'avgchart': avgchart, 'totchart': totchart, 'users': users}
    return render(request, 'consumption/summary.html', context)

def detail(request):
    context = {
    }
    return render(request, 'consumption/detail.html', context)
