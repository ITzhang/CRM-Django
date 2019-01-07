"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 登录，注册，注销，忘记密码，验证码
    path('login/', views.login, name='login'),
    path('get_valid_code/', views.get_valid_code, name='valid_code'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('sign_out/', views.logout, name='sing_out'),

    # 首页
    path('index/', views.index, name='index'),
    path('', views.login),

    # 客户管理
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/all/', views.CustomerView.as_view(), name='customer_all'),
    path('customer/add/', views.AddEditCustomerView.as_view(), name='customer_add'),
    # 添加公有用户
    path('customer/public_add/', views.AddEditCustomerView.as_view(), name='customer_public_add'),
    path('my_customer/', views.CustomerView.as_view(), name='my_customer'),
    re_path('^customer/edit/(\d+)/$', views.AddEditCustomerView.as_view(), name='customer_edit'),

    # 跟进记录管理
    path('consult_record/', views.ConsultRecordView.as_view(), name='consult_record'),
    path('consult_record/add/', views.AddEditConsultRecordView.as_view(), name='consult_record_add'),
    re_path('^consult_record/edit/(\d+)/$', views.AddEditConsultRecordView.as_view(), name='consult_record_edit'),

    # 财务管理
    path('payment/', views.PaymentView.as_view(), name='payment'),

    # 学生管理
    re_path(r'^', include('student_manage.urls')),

    # 统计数据
    path('count/customer/', views.CountCustomerView.as_view(), name='count_customer'),

    # 权限分配
    re_path(r'^', include(('rbac.urls', 'rbac'),namespace='rbac')),

]
