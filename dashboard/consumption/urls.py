from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainpage),
    url(r'^summary/', views.summary),
    url(r'^detail/', views.detail),
]
