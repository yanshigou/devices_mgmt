from django.db import models


class WFTypeModel(models.Model):
    wf_code = models.CharField(max_length=20, verbose_name="违法代码", unique=True)
    wf_name = models.CharField(max_length=20, verbose_name="违法行为")

    class Meta:
        verbose_name = "违法类型表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.wf_name


class ServerModel(models.Model):
    ip = models.CharField(max_length=15, verbose_name="服务器", unique=True)
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True, null=True)
    password = models.CharField(max_length=20, verbose_name="密码", blank=True, null=True)

    class Meta:
        verbose_name = "服务器信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class BuildCompanyModel(models.Model):
    build_company = models.CharField(max_length=30, verbose_name="建设单位", unique=True)
    name = models.CharField(max_length=10, verbose_name="联系人")
    mobile = models.CharField(max_length=15, verbose_name="联系电话")

    class Meta:
        verbose_name = '建设单位信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.build_company


class OwnerCompanyModel(models.Model):
    owner_company = models.CharField(max_length=30, verbose_name="业主单位", unique=True)
    name = models.CharField(max_length=10, verbose_name="联系人")
    mobile = models.CharField(max_length=15, verbose_name="联系电话")

    class Meta:
        verbose_name = '业主单位信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner_company


class BrigadeModel(models.Model):
    brigade = models.CharField(max_length=30, verbose_name="大队", unique=True)
    name = models.CharField(max_length=10, verbose_name="联系人")
    mobile = models.CharField(max_length=15, verbose_name="联系电话")

    class Meta:
        verbose_name = '大队信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.brigade


class RoadDeviceModel(models.Model):
    build_company = models.ForeignKey(BuildCompanyModel, verbose_name="建设单位")
    owner_company = models.ForeignKey(OwnerCompanyModel, verbose_name="业主单位")
    brigade = models.ForeignKey(BrigadeModel, verbose_name="所属大队")
    road_code = models.CharField(max_length=10, verbose_name="档案编号", unique=True)
    device_code = models.CharField(max_length=20, verbose_name="执法设备编号", unique=True, primary_key=True)
    road_name = models.CharField(max_length=30, verbose_name="路口名称", null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, verbose_name="安装地点名称")
    longitude = models.CharField(max_length=20, verbose_name='经度', null=True, blank=True)
    latitude = models.CharField(max_length=20, verbose_name='纬度', null=True, blank=True)
    time = models.DateTimeField(verbose_name="建设移交时间")
    other = models.CharField(max_length=100, verbose_name="其他信息", null=True, blank=True)
    wf_type = models.CharField(max_length=200, verbose_name="违法类型", null=True, blank=True)
    map_img = models.FileField(upload_to="road/img/", max_length=128, blank=True, null=True,
                               verbose_name='点位示意图')
    img = models.FileField(upload_to="road/img/", max_length=128, blank=True, null=True, verbose_name='现场照片')

    class Meta:
        verbose_name = '路口设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.road_name


class TerminalDeviceModel(models.Model):
    ip = models.CharField(max_length=15, verbose_name="IP地址", unique=True)
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True, null=True)
    password = models.CharField(max_length=20, verbose_name="密码", blank=True, null=True)
    server = models.ForeignKey(ServerModel, verbose_name="接入服务器", null=True, blank=True)
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备")

    class Meta:
        verbose_name = '终端设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class CameraDeviceModel(models.Model):
    ip = models.CharField(max_length=15, verbose_name="IP地址", unique=True)
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True, null=True)
    password = models.CharField(max_length=20, verbose_name="密码", blank=True, null=True)
    server = models.ForeignKey(ServerModel, verbose_name="接入服务器", null=True, blank=True)
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备")
    wf_type = models.CharField(max_length=200, verbose_name="违法类型", null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='规格型号')
    device_company = models.CharField(max_length=20, null=True, blank=True, verbose_name='厂家')
    terminal = models.ForeignKey(TerminalDeviceModel, verbose_name="接入终端", null=True, blank=True)

    class Meta:
        verbose_name = '摄像头设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class OtherDeviceModel(models.Model):
    device_name = models.CharField(max_length=10, verbose_name="设备名称")
    device_type = models.CharField(max_length=20, verbose_name="规格型号/材料")
    # device_num = models.CharField(max_length=10, verbose_name="设备数量")
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备")

    class Meta:
        verbose_name = '其他附件设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_name
