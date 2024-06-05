from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

# Create your views here.

def welcome(request):
    """欢迎界面"""
    return render(request, 'welcome.html')


def index(request):
    """防诈态势感知主界面"""
    my_range = range(1, 50)
    return render(request, 'index.html', {'my_range': my_range})


def fraud_phone_number_list(request):
    """"防诈态势感知-诈骗电话号码列表"""
    my_range = range(1, 100)
    return render(request, 'fraud_phone_number_list.html', {'my_range': my_range})


def fraud_email_list(request):
    """"防诈态势感知-诈骗邮箱列表"""
    my_range = range(1, 100)
    return render(request, 'fraud_email_list.html', {'my_range': my_range})


def fraud_ip_list(request):
    """防诈态势感知-诈骗IP列表"""
    my_range = range(1, 100)
    return render(request, 'fraud_ip_list.html', {'my_range': my_range})


def analysis_result(request):
    """分析结果页面"""
    return render(request, 'analysis_result.html')

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
