from django.db import models


# Create your models here.
# 可疑电话号码库——电话号码表
class phone_number(models.Model):
    电话号码 = models.CharField(max_length=20, primary_key=True)
    电话类型 = models.CharField(max_length=10, default=None, null=True)
    标记次数 = models.IntegerField(default=None, null=True)


# 网站网页库
# 外表
class 诈骗类型说明(models.Model):
    诈骗类型id = models.SmallIntegerField(primary_key=True)
    诈骗类型 = models.CharField(max_length=20)


# 主表
class website(models.Model):
    网站域名 = models.CharField(max_length=100, primary_key=True)
    诈骗类型 = models.ForeignKey(to="诈骗类型说明", to_field="诈骗类型id", default=None, null=True, blank=True,
                                 on_delete=models.SET_NULL)


# 短信端口库——短信表
class msg(models.Model):
    id = models.IntegerField(primary_key=True)
    短信类别 = models.SmallIntegerField()
    短信内容 = models.CharField(max_length=255)
