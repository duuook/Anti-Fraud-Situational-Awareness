from django.db import models


# Create your models here.
# 可疑电话号码——电话号码表
class phone_number(models.Model):
    电话号码 = models.CharField(max_length=20)
    电话类型 = models.CharField(max_length=10, default=None, null=True)
    标记次数 = models.IntegerField(default=None, null=True)


# 网站网页
# 外表
class 诈骗类型说明(models.Model):
    诈骗类型id = models.SmallIntegerField(primary_key=True)
    诈骗类型 = models.CharField(max_length=20)

    def __str__(self):
        return self.诈骗类型


# 主表
class website(models.Model):
    网站域名 = models.CharField(max_length=100)
    # 诈骗类型=models.ForeignKey(to="诈骗类型说明",to_field="诈骗类型id",default=None,null=True,blank=True,on_delete=models.SET_NULL)
    诈骗类型_CHOICES = (
        (0, '正常'),
        (1, '购物消费'),
        (2, '婚恋交友'),
        (3, '假冒身份'),
        (4, '钓鱼网站'),
        (5, '冒充公检法'),
        (6, '平台诈骗'),
        (7, '招聘兼职'),
        (8, '杀猪盘'),
        (9, '博彩赌博'),
        (10, '信贷理财'),
        (11, '刷单诈骗'),
        (12, '中奖诈骗'),
    )
    诈骗类型 = models.IntegerField(default=None, null=True, blank=True, choices=诈骗类型_CHOICES)


# 短信端口——短信表
class msg(models.Model):
    id = models.IntegerField(primary_key=True)
    短信类别 = models.SmallIntegerField()
    短信内容 = models.CharField(max_length=255)


# 电子邮箱——电子邮箱表
class email(models.Model):
    电子邮箱地址 = models.CharField(max_length=50)
