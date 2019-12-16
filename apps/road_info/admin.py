from django.contrib import admin
from .models import *


class WFTypeModelAdmin(admin.ModelAdmin):
    list_display = ('wf_code', 'wf_name')


class ServerModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'password')


class BuildCompanyModelAdmin(admin.ModelAdmin):
    list_display = ('build_company', 'name', 'mobile')


class OwnerCompanyModelAdmin(admin.ModelAdmin):
    list_display = ('owner_company', 'name', 'mobile')


class BrigadeModelAdmin(admin.ModelAdmin):
    list_display = ('brigade', 'name', 'mobile')


class RoadDeviceModelAdmin(admin.ModelAdmin):
    list_display = (
                    'address', 'owner_company', 'brigade', 'road_code', 'device_code', 'road_name', 'build_company',
                    'longitude', 'latitude', 'time', 'other', 'map_img', 'img', 'wf_type'
                    )


class TerminalDeviceModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'password', 'server', 'road_device')


class CameraDeviceModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'password', 'server', 'road_device', 'wf_type', 'device_type', 'device_company', 'terminal')


class OtherDeviceModelAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'road_device')


admin.site.register(WFTypeModel, WFTypeModelAdmin)
admin.site.register(ServerModel, ServerModelAdmin)
admin.site.register(BuildCompanyModel, BuildCompanyModelAdmin)
admin.site.register(OwnerCompanyModel, OwnerCompanyModelAdmin)
admin.site.register(BrigadeModel, BrigadeModelAdmin)
admin.site.register(RoadDeviceModel, RoadDeviceModelAdmin)
admin.site.register(TerminalDeviceModel, TerminalDeviceModelAdmin)
admin.site.register(CameraDeviceModel, CameraDeviceModelAdmin)
admin.site.register(OtherDeviceModel, OtherDeviceModelAdmin)
