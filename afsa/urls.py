"""afsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SE import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('afsa/', views.index),

    # 分析结果页面
    path('analysis_result/', views.analysis_result),

    # 信息库
    path('fraud_phone_number/', views.fraud_phone_number_list),
    path('fraud_msg/', views.fraud_msg_list),
    path('fraud_email/', views.fraud_email_list),
    path('fraud_ip/', views.fraud_ip_list),

    # ajax提交测试
    path('ajax/', views.ajax),

    # 历史分析查询页面
    path('history/', views.history),
]
