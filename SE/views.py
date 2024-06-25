import json
from SE.LSTM import LSTM
from SE.NLP.func import NLP
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from SE.utils.db_modelform import *  # 这里的前驱路径需要完整打出
from SE.utils.pagination import Pagination


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
    if request.method == 'GET':
        # 获取筛选数据：
        # sphone为筛选电话号码字段，stype为筛选类型
        type_choices = (
            (0, '正常'),
            (1, '诈骗电话'),
            (2, '骚扰电话'),
            (3, '非法业务'),
            (4, '网贷催收'),
            (5, '广告推销'),
            (6, '多多跨境'),
            (7, '响一声挂')
        )
        filter_phone_condition = request.GET.get('sphone', '')
        filter_type_condition = request.GET.get('stype', '')

        # 获取数据库总条数以及筛选后的数据
        if filter_type_condition != '0' and filter_type_condition != '':
            phone_numbers = models.phone_number.objects.filter(电话号码__contains=filter_phone_condition,
                                                               电话类型=filter_type_condition)
        else:
            phone_numbers = models.phone_number.objects.filter(电话号码__contains=filter_phone_condition)

        # 分页设计:
        page_object = Pagination(request, filter_ip_content=phone_numbers, plus=10, method=request.method)

        # 传递数据字典
        context = {'phone_numbers': page_object.filter_ip_content, 'filter_condition': filter_phone_condition,
                   'type_choices': type_choices, 'page_str': page_object.html(), 'total_page': page_object.total_page,
                   'current_page': page_object.page}
        return render(request, 'fraud_phone_number_list.html', context)


def fraud_msg_list(request):
    """"防诈态势感知-诈骗短信列表"""
    if request.method == 'GET':
        filter_msg_content = models.msg.objects.filter(短信类别=1)

        # 分页设计:
        page_object = Pagination(request, filter_ip_content=filter_msg_content, plus=10, method=request.method)

        # 传递数据字典
        context = {
            'msgs': page_object.filter_ip_content,
            'page_str': page_object.html(),
            'total_page': page_object.total_page,
            'current_page': page_object.page
        }
        return render(request, 'fraud_msg_list.html', context)


@csrf_exempt
def fraud_ip_list(request):
    """防诈态势感知-诈骗IP列表"""
    if request.method == 'GET':
        # 获取筛选数据：
        # sip为筛选IP，stype为筛选类型
        type_choices = models.website.诈骗类型_CHOICES
        filter_ip_condition = request.GET.get('sip', '')
        filter_type_condition = request.GET.get('stype', '')

        # 获取数据库总条数以及筛选后的数据
        if filter_type_condition != '0' and filter_type_condition != '':
            filter_ip_content = models.website.objects.filter(网站域名__contains=filter_ip_condition,
                                                              诈骗类型=filter_type_condition)
        else:
            filter_ip_content = models.website.objects.filter(网站域名__contains=filter_ip_condition)

        # 分页设计:
        page_object = Pagination(request, filter_ip_content=filter_ip_content, plus=10, method=request.method)

        # 传递数据字典
        context = {'websites': page_object.filter_ip_content, 'filter_condition': filter_ip_condition,
                   'type_choices': type_choices, 'page_str': page_object.html(), 'total_page': page_object.total_page,
                   'current_page': page_object.page}

        return render(request, 'fraud_ip_list.html', context)


def fraud_email_list(request):
    """防诈态势感知-诈骗邮箱列表"""
    if request.method == 'GET':
        # 获取筛选数据：
        # semail为筛选邮箱字段
        filter_email_condition = request.GET.get('semail', '')

        # 获取数据库总条数以及筛选后的数据
        filter_email_content = models.email.objects.filter(电子邮箱地址__contains=filter_email_condition)

        # 分页设计:
        page_object = Pagination(request, filter_ip_content=filter_email_content, plus=10, method=request.method)

        # 传递数据字典
        context = {'email_list': page_object.filter_ip_content, 'filter_condition': filter_email_condition,
                   'page_str': page_object.html(), 'total_page': page_object.total_page,
                   'current_page': page_object.page}
        return render(request, 'fraud_email_list.html', context)


@csrf_exempt
def analysis_result(request):
    """分析结果页面"""
    if request.method == 'GET':
        data = request.GET.get('input')
        stype = request.GET.get('stype')
        print(data, stype)

        # ----------------------------服务函数-------------------------------------
        if stype == 'text_analysis':
            # 文本分析
            analysis_report = LSTM.text_analysis(data)
            # 错误处理
            if analysis_report['Get_keywords_report']['status'] == 0:
                context = {
                    "error": analysis_report['Get_keywords_report']['error'],
                }
                return render(request, 'analysis_error.html', context)
            elif analysis_report['Text_predict_report']['status'] == 0:
                context = {
                    "error": analysis_report['Text_predict_report']['error'],
                }
                return render(request, 'analysis_error.html', context)
            context = {
                'Get_keywords_report': analysis_report['Get_keywords_report'],
                'Text_predict_report': analysis_report['Text_predict_report'],
            }
            return render(request, 'text_analysis_result.html', context)
        if stype == 'ip':
            # 网页分析
            ip_analysis_report = NLP.websit_analysis(data)
        return render(request, 'text_analysis_result.html')

    if request.method == 'POST':
        # 获取前端传递的数据
        stype = request.POST.get('stype')
        data = request.POST.get('input')
        print(data, stype)
        if stype == 'text_analysis':
            response = {
                'status': 200,
                'message': '提交成功'
            }
        if stype == 'phone':
            Query_report = LSTM.phonenumber_query(data)
            response = Query_report['phonenumber_query_result']

            location_report = LSTM.phone_number_location(data)
            if location_report['status']:
                response['省份'] = location_report['省份']
                response['城市'] = location_report['城市']
                response['运营商'] = location_report['运营商']
                response['区号'] = location_report['区号']

        if stype == 'ip':
            Query_report = LSTM.ip_query(data)
            response = Query_report['ip_query_result']
        if stype == 'email':
            Query_report = LSTM.emails_query(data)
            response = Query_report['emails_query_result']

        print(response)
        return HttpResponse(json.dumps(response))


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


def history(request):
    """历史分析查询页面"""
    if request.method == 'GET':
        # 获取数据库总条数以及筛选后的数据
        history_data = models.history.objects.all()

        # 分页设计:
        page_object = Pagination(request, filter_ip_content=history_data, plus=10, method=request.method)

        # 传递数据字典
        context = {'history_data': page_object.filter_ip_content, 'page_str': page_object.html(),
                   'total_page': page_object.total_page, 'current_page': page_object.page}
        return render(request, 'history.html', context)
    return None
