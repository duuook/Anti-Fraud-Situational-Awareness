from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from SE.utils.db_modelform import *  # 这里的前驱路径需要完整打出


# Create your views here.

def welcome(request):
    """欢迎界面"""
    return render(request, 'welcome.html')


def index(request):
    """防诈态势感知主界面"""

    chart_data = [
        models.phone_number.objects.all().count(),
        models.website.objects.all().count(),
        models.msg.objects.all().count(),
        models.email.objects.all().count(),
    ]
    slim_data = {
        'phone_number_slim': models.phone_number.objects.all()[:100],
        'email_slim': models.email.objects.all()[:100],
        'ip_slim': models.website.objects.all()[:100],
        'chart_data': chart_data,
    }
    return render(request, 'index.html', slim_data)


def fraud_phone_number_list(request):
    """"防诈态势感知-诈骗电话号码列表"""
    my_range = range(1, 100)
    """
    # 此处用以填充数据库相关操作内容
    """
    if request.method == 'GET':
        form = PhoneNumberModelForm()
        phone_numbers = models.phone_number.objects.all()
        return render(request, 'fraud_phone_number_list.html', {'form': form, 'phone_numbers': phone_numbers})

    return render(request, 'fraud_phone_number_list.html', {'my_range': my_range})


def fraud_msg_list(request):
    """"防诈态势感知-诈骗短信列表"""
    # my_range = range(1, 100)

    if request.method == 'GET':
        form = msgModelForm()
        msgs = models.msg.objects.filter(短信类别=1)
        return render(request, 'fraud_msg_list.html', {'form': form, 'msgs': msgs})


def fraud_ip_list(request):
    """防诈态势感知-诈骗IP列表"""
    if request.method == 'GET':
        form = WebsiteModelForm()
        websites = models.website.objects.all()
        return render(request, 'fraud_ip_list.html', {'form': form, 'websites': websites})


def fraud_email_list(request):
    """防诈态势感知-诈骗邮箱列表"""
    email_list = models.email.objects.all()

    return render(request, 'fraud_email_list.html', {'email_list': email_list})


def analysis_result(request):
    """分析结果页面"""
    if request.method == 'GET':
        return render(request, 'analysis_result.html')

    if request.method == 'POST':
        # 获取前端传递的数据
        data = request.POST
        print(data)


@csrf_exempt
def ajax(request):
    """ajax提交测试"""
    message = request.POST
    print(message)

    response = {
        'status': 200,
        'message': '提交成功'
    }
    return HttpResponse(json.dumps(response))
