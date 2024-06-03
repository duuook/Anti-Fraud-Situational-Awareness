import datetime

from django.db import models


# Create your models here.
class FraudPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=15)
    create_time = models.DateTimeField(auto_now_add=True)



class FraudEmail(models.Model):
    email = models.EmailField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)


class FraudIP(models.Model):
    """诈骗网站"""
    # 诈骗IP
    ip = models.GenericIPAddressField()
    # 诈骗网址
    url = models.URLField()
    # 诈骗网站名称
    name = models.CharField(max_length=50)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
