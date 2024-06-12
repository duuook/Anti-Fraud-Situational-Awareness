from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
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
        # 获取筛选数据：
        # sip为筛选IP，stype为筛选类型
        type_choices = models.website.诈骗类型_CHOICES
        filter_ip_condition = request.GET.get('sip', '')
        filter_type_condition = request.GET.get('stype', '')

        # 分页设计:
        #   每页都是十条数据，根据前端传递的页码进行分页
        page = int(request.GET.get('page', 1))
        page_size = 10
        start = (page - 1) * page_size
        end = page * page_size

        # 获取数据库总条数以及筛选后的数据
        if filter_type_condition != '0' and filter_type_condition != '':
            filter_ip_content = models.website.objects.filter(网站域名__contains=filter_ip_condition,
                                                              诈骗类型=filter_type_condition)[start:end]
            total_count = models.website.objects.filter(网站域名__contains=filter_ip_condition,
                                                        诈骗类型=filter_type_condition).count()
        else:
            filter_ip_content = models.website.objects.filter(网站域名__contains=filter_ip_condition)[start:end]
            total_count = models.website.objects.filter(网站域名__contains=filter_ip_condition).count()

        # 页码
        # 1. 总页码
        total_page, m = divmod(total_count, page_size)
        if m:
            total_page += 1

        # 2. 生成页码
        #   只显示前五页和后五页
        if total_page < 11:
            page_start = 1
            page_end = total_page + 1
        else:
            if page < 6:
                page_start = 1
                page_end = 11
            else:
                if page + 5 > total_page:
                    page_start = total_page - 9
                    page_end = total_page + 1
                else:
                    page_start = page - 5
                    page_end = page + 6

        page_str_list = []

        # 首页
        first = '<li><a href="?page=1"><span aria-hidden="true">首页</span></a></li>'
        page_str_list.append(first)

        # 上一页
        if page == 1:
            prev = '<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            prev = '<li><a href="?page=%s"><span aria-hidden="true">&laquo;</span></a></li>' % (page - 1)
        page_str_list.append(prev)

        for i in range(page_start, page_end):
            if i == page:
                temp = '<li class="active"><a href="?page=%s">%s</a></li>' % (i, i)
            else:
                temp = '<li><a href="?page=%s">%s</a></li>' % (i, i)
            page_str_list.append(temp)

        # 下一页
        if page == total_page:
            after = '<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            after = '<li><a href="?page=%s"><span aria-hidden="true">&raquo;</span></a></li>' % (page + 1)
        page_str_list.append(after)

        # 尾页
        last = '<li><a href="?page=%s"><span aria-hidden="true">尾页</span></a></li>' % total_page
        page_str_list.append(last)

        """
        <li><a href="?page=2#">2</a></li
        <li><a href="?page=3">3</a></li>
        <li><a href="?page=4">4</a></li>
        <li><a href="?page=5">5</a></li>
        """

        # 跳转框
        jump = """<li>
                    <form method="get" style="float: left;margin-left: -1px">
                        <input name="page"
                               style="position: relative;float: left;display: inline-block;width: 100px;border-radius:0 "
                               type="number" class="form-control" placeholder="页码">
                        <button id="jump-button" class="btn btn-default" type="submit">跳转</button>
                    </form>
                </li>
                """
        page_str_list.append(jump)

        page_str = mark_safe(''.join(page_str_list))

        return render(request, 'fraud_ip_list.html',
                      {'websites': filter_ip_content, 'filter_condition': filter_ip_condition,
                       'type_choices': type_choices, 'page_str': page_str, 'total_page': total_page,
                       'current_page': page})


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
