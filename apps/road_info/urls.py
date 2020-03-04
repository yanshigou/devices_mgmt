# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2020/3/4"
from django.conf.urls import url
from .views import ShowMapView

urlpatterns = [
    url(r'^map/$', ShowMapView.as_view(), name='show_map'),
]
