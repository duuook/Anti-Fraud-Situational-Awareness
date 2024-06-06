from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django import forms
from SE import models

# Create your views here.

def welcome(request):
    """欢迎界面"""
    return render(request, 'welcome.html')


def index(request):
    """防诈态势感知主界面"""
    my_range = range(1, 50)
    return render(request, 'index.html', {'my_range': my_range})


class PhoneNumberModelForm(forms.ModelForm):
    class Meta:
        model = models.phone_number
        fields = ['电话号码', '电话类型', '标记次数']

    def __init__(self, *args, **kwargs):
        super(PhoneNumberModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}



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


class msgModelForm(forms.ModelForm):
    class Meta:
        model = models.msg
        fields = ['id', '短信类别', '短信内容']

    # def __init__(self, *args, **kwargs):
    #     super(msgModelForm, self).__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {'class': 'form-control'}


def fraud_email_list(request):
    """"防诈态势感知-诈骗邮箱列表"""
    # my_range = range(1, 100)

    if request.method == 'GET':
        form = msgModelForm()
        msgs = models.msg.objects.all()
        return render(request, 'fraud_msg_list.html', {'form': form, 'msgs': msgs})


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
