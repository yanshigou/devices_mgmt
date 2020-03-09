# -*- coding: utf-8 -*-
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import *
from myutils.utils import export_excel, bd09_to_gcj02
from datetime import datetime
from devices_mgmt.settings import MEDIA_ROOT
from django.shortcuts import render


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


class ExportView(View):
    def get(self, request):
        road_device = RoadDeviceModel.objects.all()
        data_list = list()
        for i in road_device:
            camera_list = list()
            terminal_list = list()
            other_list = list()
            owner_company = i.owner_company
            if owner_company:
                owner_company = owner_company.owner_company
            else:
                owner_company = ""
            build_company = i.build_company
            if build_company:
                build_company = build_company.build_company
            else:
                build_company = ""
            brigade = i.brigade
            if brigade:
                brigade = brigade.brigade
            else:
                brigade = ""
            time = i.time
            if time:
                time = datetime.strftime(time, "%Y{}%m{}%d{}").format("年", "月", "日")
            else:
                time = ""

            longitude = i.longitude
            latitude = i.latitude
            if longitude and latitude:
                longitude_latitude = longitude + "," + latitude
            else:
                longitude_latitude = ""
            src = MEDIA_ROOT + '/%s' % i.map_img
            src2 = MEDIA_ROOT + '/%s' % i.img
            camera_device = CameraDeviceModel.objects.filter(road_device_id=i.id)
            # print(camera_device)
            for c in camera_device:
                terminal = c.terminal
                if terminal:
                    terminal = terminal.ip
                else:
                    terminal = ""
                server = c.server
                if server:
                    server = server.ip
                else:
                    server = ""
                wf_type = c.wf_type
                if wf_type:
                    wf_type = ",".join(wf_type)
                else:
                    wf_type = ""
                username = c.username
                if not username:
                    username = ""
                password = c.password
                if not password:
                    password = ""
                camera_list.append({
                    "ip": c.ip,
                    "device_type": c.device_type,
                    "username_pwd": username + "/" + password,
                    "terminal": terminal,
                    "server": server,
                    "wf_type": wf_type
                })
            terminal_device = TerminalDeviceModel.objects.filter(road_device_id=i.id)
            for t in terminal_device:
                server = t.server
                if server:
                    server = server.ip
                else:
                    server = ""
                terminal_list.append({
                    "ip": t.ip,
                    "device_type": t.device_type,
                    "username_pwd": t.username + "/" + t.password,
                    "terminal": "",
                    "server": server,
                    "wf_type": ""
                })
            other_device = OtherDeviceModel.objects.filter(road_device_id=i.id)
            for o in other_device:
                other_list.append({
                    "device_name": o.device_name,
                    "device_type": o.device_type,
                    "device_num": o.device_num
                })

            data_list.append({
                "road_type": i.get_road_type_display(),
                "road_code": i.road_code,
                "address": i.address,
                "owner_company": owner_company,
                "longitude_latitude": longitude_latitude,
                "build_company": build_company,
                "device_code": i.device_code,
                "brigade": brigade,
                "time": time,
                "camera_list": camera_list,
                "terminal_list": terminal_list,
                "other_list": other_list,
                "map_img": src,
                "img2": src2

            })

        save_file = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S") + ".xlsx"
        folder = "/".join((MEDIA_ROOT + "\\" + save_file).split("\\"))
        # url = "192.168.31.54:9999/media/" + save_file
        url = "111.230.246.188:8888/media/" + save_file
        export_excel(data_list, folder)
        return HttpResponse(url)


class ModifyRoadCodeView(View):
    def get(self, request):
        try:
            wt_road = RoadDeviceModel.objects.all()
            for i in wt_road:
                i.road_code = i.device_code[-5:]
                i.save()
        except Exception as e:
            return JsonResponse({
                "status": "fail",
                "error": str(e)
            })
        return JsonResponse({
            "status": "success"
        })


class ShowMapView(View):
    def get(self, request):
        file = MEDIA_ROOT + '\\wt.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='wt')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\dj.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='dj')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\bd.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='bd')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\cs.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='cs')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\xr.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='xr')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\md.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='md')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\wjl.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='wjl')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\kk.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='kk')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        file = MEDIA_ROOT + '\\jk.txt'
        all_devices = RoadDeviceModel.objects.filter(road_type='jk')
        f = open(file, 'w+', encoding='utf-8')
        for i in all_devices:
            longitude = i.longitude
            latitude = i.latitude
            address = i.address
            r_id = str(i.id)
            c = CameraDeviceModel.objects.filter(road_device_id=r_id)
            c_ip = ""
            for x in c:
                c_ip += x.ip + "-"

            t = TerminalDeviceModel.objects.filter(road_device_id=r_id)
            t_ip = ""
            for u in t:
                t_ip += u.ip + '-'
            # 百度坐标转换为高德坐标
            if longitude and latitude:
                if len(latitude) > 4 and len(longitude) > 3:
                    lon, lat = bd09_to_gcj02(float(longitude), float(latitude))
                    a = str(lon) + ',' + str(lat) + ',' + address + ',' + r_id + "," + c_ip + "," + t_ip + '\n'
                    f.write(a)
        f.close()
        # return render(request, "map.html", {})
        return render(request, "cq.html", {})
