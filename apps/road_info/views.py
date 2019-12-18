# -*- coding: utf-8 -*-
from django.views import View
from django.http import JsonResponse
from .models import *


class Test(View):

    def post(self, request):
        d_type = request.POST.get('d_type')
        camera_ip = request.POST.get('camera_ip')
        terminal_ip = request.POST.get('terminal_ip')
        password = request.POST.get('password')
        device_code = request.POST.get('device_code')
        address = request.POST.get('address')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        device_company = request.POST.get('device_company')
        device_type = request.POST.get('device_type')
        server = request.POST.get('server')
        time = request.POST.get('time')
        other = request.POST.get('other')
        owner_company = request.POST.get('owner_company')
        build_company = request.POST.get('build_company')
        road_code = request.POST.get('road_code')

        try:
            a = RoadDeviceModel.objects.filter(device_code=device_code)

            if not a:
                if owner_company and build_company:
                    road = RoadDeviceModel.objects.create(road_type=d_type, build_company_id=build_company,
                                                          owner_company_id=owner_company,
                                                          device_code=device_code, road_code=road_code, address=address,
                                                          longitude=longitude, latitude=latitude, time=time,
                                                          other=other)
                elif build_company and not owner_company:
                    road = RoadDeviceModel.objects.create(road_type=d_type, build_company_id=build_company,
                                                          device_code=device_code, road_code=road_code, address=address,
                                                          longitude=longitude, latitude=latitude, time=time,
                                                          other=other)
                else:
                    road = RoadDeviceModel.objects.create(road_type=d_type,
                                                          device_code=device_code, road_code=road_code, address=address,
                                                          longitude=longitude, latitude=latitude, time=time,
                                                          other=other)
                road_device_id = road.id
            else:
                road_device_id = a[0].id
            # print('r_id', road_device_id)
            b = TerminalDeviceModel.objects.filter(ip=terminal_ip)

            if not b:
                termainal = TerminalDeviceModel.objects.create(ip=terminal_ip, username='admin', password=password,
                                                               server_id=server, road_device_id=road_device_id,
                                                               device_type=device_type, device_company=device_company)
                terminal_id = termainal.id
            else:
                terminal_id = b[0].id
            # print('t_id', terminal_id)
            c = CameraDeviceModel.objects.filter(ip=camera_ip)
            if not c:
                camera = CameraDeviceModel.objects.create(ip=camera_ip, username='admin', password=password,
                                                          server_id=server, road_device_id=road_device_id,
                                                          wf_type="10395",
                                                          device_type=device_type, device_company=device_company,
                                                          terminal_id=terminal_id)
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": "fail"
            })
        return JsonResponse({
            "status": "success"
        })
