from django.db import models
from multiselectfield import MultiSelectField


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
    name = models.CharField(max_length=10, verbose_name="联系人", blank=True, null=True)
    mobile = models.CharField(max_length=15, verbose_name="联系电话", blank=True, null=True)

    class Meta:
        verbose_name = '建设单位信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.build_company


class OwnerCompanyModel(models.Model):
    owner_company = models.CharField(max_length=30, verbose_name="业主单位", unique=True)
    name = models.CharField(max_length=10, verbose_name="联系人", blank=True, null=True)
    mobile = models.CharField(max_length=15, verbose_name="联系电话", blank=True, null=True)

    class Meta:
        verbose_name = '业主单位信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner_company


class BrigadeModel(models.Model):
    brigade = models.CharField(max_length=30, verbose_name="大队", unique=True)
    name = models.CharField(max_length=10, verbose_name="联系人", blank=True, null=True)
    mobile = models.CharField(max_length=15, verbose_name="联系电话", blank=True, null=True)

    class Meta:
        verbose_name = '大队信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.brigade


class RoadDeviceModel(models.Model):
    road_type = models.CharField(max_length=40, choices=(
        ('wt', '违停'), ('dj', '电警'), ('bd', '变道抓拍'), ('cs', '超速'), ('xr', '礼让行人'),
        ('md', '违法鸣笛'), ('wjl', '违禁令'), ('kk', '卡口'), ('jk', '高空监控')
    ), verbose_name="设备类型")
    build_company = models.ForeignKey(BuildCompanyModel, verbose_name="建设单位", blank=True, null=True)
    owner_company = models.ForeignKey(OwnerCompanyModel, verbose_name="业主单位", blank=True, null=True)
    brigade = models.ForeignKey(BrigadeModel, verbose_name="所属大队", blank=True, null=True)
    road_code = models.CharField(max_length=10, verbose_name="档案编号", unique=True)
    device_code = models.CharField(max_length=20, verbose_name="执法设备编号", blank=True, null=True, unique=True)
    address = models.CharField(max_length=200, verbose_name="安装地点名称")
    longitude = models.CharField(max_length=30, verbose_name='经度', null=True, blank=True)
    latitude = models.CharField(max_length=30, verbose_name='纬度', null=True, blank=True)
    time = models.DateField(verbose_name="建设移交时间", null=True, blank=True)
    other = models.CharField(max_length=200, verbose_name="其他信息", null=True, blank=True)
    map_img = models.FileField(upload_to="road/img/", max_length=128, blank=True, null=True,
                               verbose_name='点位示意图')
    img = models.FileField(upload_to="road/img/", max_length=128, blank=True, null=True, verbose_name='现场照片')

    class Meta:
        verbose_name = '路口设备信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class TerminalDeviceModel(models.Model):
    ip = models.CharField(max_length=15, verbose_name="应指网IP")
    port = models.CharField(max_length=15, verbose_name="应指网端口", default='80')
    local_ip = models.CharField(max_length=15, verbose_name="局域网IP", blank=True, null=True)
    local_port = models.CharField(max_length=15, verbose_name="局域网端口", blank=True, null=True)
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True, null=True, default="admin")
    password = models.CharField(max_length=20, verbose_name="密码", blank=True, null=True, default="hik12345")
    server = models.ForeignKey(ServerModel, verbose_name="接入服务器", null=True, blank=True)
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备", null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='规格型号')
    device_company = models.CharField(max_length=20, null=True, blank=True, verbose_name='厂家',
                                      choices=(('hk', '海康'), ('kd', '科达'), ('dh', '大华')))

    class Meta:
        verbose_name = '终端设备信息'
        verbose_name_plural = verbose_name
        unique_together = ("ip", "port")

    def __str__(self):
        return self.ip + ":" + self.port


wf_types = (('13443', '违反禁令标志'),
            ('13011', '逆行'),
            ('13452', '违反禁止标线'),
            ('13452', '违反禁止停车标线'),
            ('10192', '违反规定使用专用车道'),
            ('16250', '违反交通信号灯'),
            ('12082', '不按导向车道行驶'),
            ('12231', '开车打电话'),
            ('13571', '不礼让斑马线'),
            ('10482', '违法鸣笛'),
            ('13442', '载货汽车限行'),
            ('60112', '不系安全带'),
            ('10395', '违法停车'),
            ('1352', '超速'))


class CameraDeviceModel(models.Model):
    ip = models.CharField(max_length=15, verbose_name="应指网IP")
    port = models.CharField(max_length=15, verbose_name="应指网端口", default='80')
    local_ip = models.CharField(max_length=15, verbose_name="局域网IP", blank=True, null=True)
    local_port = models.CharField(max_length=15, verbose_name="局域网端口", blank=True, null=True)
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True, null=True, default="admin")
    password = models.CharField(max_length=20, verbose_name="密码", blank=True, null=True, default="hik12345")
    server = models.ForeignKey(ServerModel, verbose_name="接入服务器", null=True, blank=True)
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备", null=True, blank=True)
    wf_type = MultiSelectField('违法代码', choices=wf_types, null=True, blank=True)
    # wf_type = models.CharField(max_length=200, verbose_name="违法类型", null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='规格型号')
    device_company = models.CharField(max_length=20, null=True, blank=True, verbose_name='厂家',
                                      choices=(('hk', '海康'), ('kd', '科达')))
    terminal = models.ForeignKey(TerminalDeviceModel, verbose_name="接入终端", null=True, blank=True)

    class Meta:
        verbose_name = '摄像机设备信息'
        verbose_name_plural = verbose_name
        unique_together = ("ip", "port")

    def __str__(self):
        return self.ip + ":" + self.port


class OtherDeviceModel(models.Model):
    device_name = models.CharField(max_length=10, verbose_name="设备名称")
    device_type = models.CharField(max_length=20, verbose_name="规格型号/材料", blank=True, null=True)
    device_num = models.IntegerField(default=1, verbose_name="设备数量")
    road_device = models.ForeignKey(RoadDeviceModel, verbose_name="所属路口设备", blank=True, null=True)

    class Meta:
        verbose_name = '其他附件设备信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_name
