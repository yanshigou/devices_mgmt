"""devices_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from .settings import MEDIA_ROOT
from road_info.views import Test, ExportView, ModifyRoadCodeView, ShowMapView


urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^test/$', Test.as_view()),
    url(r'^export/$', ExportView.as_view()),
    url(r'^map/$', ShowMapView.as_view(), name='show_map'),
    # url(r'^modifyWT/$', ModifyRoadCodeView.as_view()),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
