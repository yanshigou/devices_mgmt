from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

admin.site.site_title = "沙坪坝电子警察设备管理系统v1.0"

admin.site.site_header = "沙坪坝电子警察设备管理系统v1.0"


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


class CameraInline(admin.StackedInline):
    model = CameraDeviceModel
    extra = 0


class TerminalInline(admin.TabularInline):
    model = TerminalDeviceModel
    extra = 0


class OtherInline(admin.TabularInline):
    model = OtherDeviceModel
    extra = 0


class RoadDeviceModelAdmin(admin.ModelAdmin):
    list_display = (
        'address', 'road_code', 'device_code', 'road_type', 'wftype', 'terminal', 'camera', 'brigade',
        'build_company', 'time', 'map_img2', 'img2'
    )
    list_filter = ('road_type', 'build_company')
    search_fields = ['address', 'road_code', 'cameradevicemodel__ip', 'terminaldevicemodel__ip']

    inlines = [CameraInline, TerminalInline, OtherInline]

    # 'other', 'map_img', 'img', 'longitude', 'latitude', 'owner_company',

    def wftype(self, obj):
        lwfs = [tt.wf_type for tt in CameraDeviceModel.objects.filter(
            road_device=obj)]
        wflist = []
        for lwf in lwfs:
            for ll in lwf:
                # print(ll)
                if not (ll in wflist):
                    wflist.append(ll)
        return wflist[:]

    wftype.short_description = "违法代码"

    def terminal(self, obj):
        return [tt.ip for tt in TerminalDeviceModel.objects.filter(road_device=obj)]

    terminal.short_description = "终端"

    def camera(self, obj):
        return [tt.ip for tt in CameraDeviceModel.objects.filter(road_device=obj)]

    camera.short_description = "相机"

    def map_img2(self, obj):
        str_html = ""
        if obj.map_img:
            str_html += '<a href="%s" target="_blank"><img src="%s" width="50px" /><a/>' % (obj.map_img.url, obj.map_img.url)
        return mark_safe(str_html)

    map_img2.short_description = "点位示意图"

    def img2(self, obj):
        str_html = ""
        if obj.img:
            str_html += '<a href="%s" target="_blank"><img src="%s" width="50px" /><a/>' % (obj.img.url, obj.img.url)
        return mark_safe(str_html)

    img2.short_description = "现场照片"


class TerminalDeviceModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'password', 'server', 'road_device')
    search_fields = ['ip', 'road_device__address']


class CameraDeviceModelAdmin(admin.ModelAdmin):
    list_display = (
        'ip', 'username', 'password', 'server', 'road_device', 'wf_type', 'device_type', 'device_company', 'terminal',
    )
    search_fields = ['ip', 'road_device__address', 'wf_type']


class OtherDeviceModelAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'road_device')
    search_fields = ['device_name', 'device_type', 'road_device__address']


admin.site.register(WFTypeModel, WFTypeModelAdmin)
admin.site.register(ServerModel, ServerModelAdmin)
admin.site.register(BuildCompanyModel, BuildCompanyModelAdmin)
admin.site.register(OwnerCompanyModel, OwnerCompanyModelAdmin)
admin.site.register(BrigadeModel, BrigadeModelAdmin)
admin.site.register(RoadDeviceModel, RoadDeviceModelAdmin)
admin.site.register(TerminalDeviceModel, TerminalDeviceModelAdmin)
admin.site.register(CameraDeviceModel, CameraDeviceModelAdmin)
admin.site.register(OtherDeviceModel, OtherDeviceModelAdmin)
