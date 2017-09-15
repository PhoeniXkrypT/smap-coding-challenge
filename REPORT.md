# Implementation
Implemented both summary view and detail view.

## Databases
There are two databases: UserData and ConsumptionData which will be
populated by data from the userdata and user consumption data files.
``python manage.py import`` populates the databases. The import may take few
minutes depending on size/number of files.
The path to data is set in ``settings.py`` as ``DATA_PATH``.

## Chart
The charts are based on 'django-graphos'. In summary view, AreaChart is
used for average consumption whereas LineChart is used for total consumption
data. In detail view, LineChart of average energy consumption is shown.

## Table
The user data table is displayed using 'django-tables2' and the table can
be displayed with any of the fields in sorted order by clicking on the
field name. By default it is displayed based on 'Userid' field.

Some customization of the table can be done using djangotables2 tables.

## Loading
The loading of summary page takes about 6 seconds due to the aggregate function.
But since the aggregate is called only once for both average and total consumption calculation, the delay is not doubled. The same delay occurs when the ``Next`` option
of table is pressed, as it loads the page again.
The table can be displayed completely in one page, this would avoid the
relaoding when next page is taken but the scroll of the page gets longer
as the user numbers grow. The user table can also be split and shown as below:
``Userid Area Tariff        Userid Area Tariff``.
