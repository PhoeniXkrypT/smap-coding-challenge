from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainpage),
    url(r'^summary/', views.summary),
    url(r'^detail/([0-9]{4,5})', views.user_detail, name='user_detail'),
    url(r'^detail/', views.detail),
]
