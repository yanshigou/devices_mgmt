from __future__ import unicode_literals
from django.db import models

# 继承自带的User表 再添加需要的其他字段
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, verbose_name='姓名', default='')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系电话')

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
