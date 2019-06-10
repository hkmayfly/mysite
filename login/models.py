from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class User(models.Model):
    '''用户表'''
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):  # 一对一保存用户与注册码之间的关系
    code = models.CharField(max_length=256)  # 哈希之后的注册码
    user = models.OneToOneField('User', on_delete=models.CASCADE)  # 关联的OTO的USER
    c_time = models.DateTimeField(auto_now_add=True)  # 注册提交时间

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]  # 注册提交时间排序
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
