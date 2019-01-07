from django.shortcuts import render, HttpResponse, redirect
from app01.utils.valid_code import get_valid_img
from app01.utils.forms_check import RegModelForm, CustomerModelForm, ConsultRecordModelForm
from app01.utils.pages import Pagination
from app01.models import UserInfo, Customer, ConsultRecord, ClassList, enroll_status_choices
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import auth
from django.views import View
from rbac.utils.reg_session import initial_session
import datetime
import copy


# Create your views here.


def login(request):
    """
    登录: 基于ajax请求的登录功能
    :param request:
    :return:
    """
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')

        response = {'username': None, 'error': None, 'next_path': reverse('index')}
        if valid_code.upper() == request.session.get('code_str').upper():
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                response['username'] = username
                # 注入权限session
                initial_session(user_obj, request)
            else:
                response['error'] = '用户名密码错误'
        else:
            response['error'] = '验证码错误'
        # 页面上下文
        next_path = request.GET.get('next')
        if next_path:
            response['next_path'] = next_path

        return JsonResponse(response)

    return render(request, 'login.html')


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('login')


def get_valid_code(request):
    """
    验证码
    :param request:
    :return:
    """
    code_img, code_str = get_valid_img()
    request.session['code_str'] = code_str
    return HttpResponse(code_img)


def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'admin-index.html')


class RegisterView(View):
    """
    注册（基于ajax和modelform的注册）
    """

    def get(self, request):
        forms = RegModelForm()
        return render(request, 'register.html', {'forms': forms})

    def post(self, request):
        forms = RegModelForm(request.POST)
        response = {'username': None, 'error': None}
        if forms.is_valid():
            forms.cleaned_data.pop('confirm_password')
            UserInfo.objects.create_user(**forms.cleaned_data)
            response['username'] = forms.cleaned_data.get('username')
        else:
            response['error'] = forms.errors
        return JsonResponse(response)


class CustomerView(View):
    """
    查看客户
    """

    def get(self, request):

        if request.path == reverse('my_customer'):
            customer_list = Customer.objects.filter(consultant=request.user)
            label = '我的客户'
        elif request.path == reverse('customer_all'):
            customer_list = Customer.objects.all()
            label = '所有客户'
        else:
            customer_list = Customer.objects.filter(consultant__isnull=True)
            label = '公有客户'
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, customer_list)
        page_html, customer_list, counter = pagination.page_html()

        class_list = ClassList.objects.all()
        consultrecord_list = UserInfo.objects.filter(positions__depart__name='销售部')

        url_parms = self.conditions(request)

        return render(request, 'customer.html',
                      {'page_html': page_html,
                       'customer_list': customer_list,
                       'counter': counter,
                       'label': label,
                       'current_page_num': current_page_num,
                       'class_list': class_list,
                       'status': enroll_status_choices,
                       'consultrecord_list': consultrecord_list,
                       'url_parms': url_parms})

    def post(self):
        pass

    def conditions(self, request):
        conditions_dict = {}
        for key, value in request.GET.items():
            if len(request.GET.getlist('consultant_id')) > 1:
                continue
            conditions_dict[key] = value

        url_parms = '&'.join(
            ['{}={}'.format(el[0], el[1]) for el in zip(conditions_dict.keys(), conditions_dict.values())]
        )
        print(url_parms)
        return url_parms


class AddEditCustomerView(View):
    """
    添加，编辑客户
    """

    def get(self, request, c_id=None):
        """
        添加/编辑客户页面
        :param request:
        :param c_id:
        :return:
        """
        customer_obj = Customer.objects.filter(pk=c_id).first()
        forms = CustomerModelForm(request, instance=customer_obj)
        return render(request, 'add_edit_customer.html', {'forms': forms, 'customer_obj': customer_obj})

    def post(self, request, c_id=None):
        """
        提交添加/编辑页面数据
        :param request:
        :param c_id: 编辑的客户id
        :return:
        """
        customer_obj = Customer.objects.filter(pk=c_id).first()
        forms = CustomerModelForm(request, data=request.POST, instance=customer_obj)
        if forms.is_valid():
            forms.save()
            next_path = request.GET.get('next', reverse('customer'))
            page = request.GET.get('page', 1)
            return redirect('{}?page={}'.format(next_path, page))
        else:
            return render(request, 'add_edit_customer.html', {'forms': forms})


class ConsultRecordView(View):
    """
    查看跟进记录
    """

    def get(self, request):
        """
        查看跟进记录
        :param request:
        :return:
        """
        # 查询指定客户的跟进记录
        cid = request.GET.get('cid')
        if cid:
            consult_record = ConsultRecord.objects.filter(customer_id=cid)
            if consult_record and not consult_record.first().consultant == request.user and consult_record.first().consultant:
                return HttpResponse('非法操作,你没有权限查看该客户的记录')
        else:
            consult_record = ConsultRecord.objects.filter(consultant=request.user)

        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, consult_record)
        page_html, consult_record, counter = pagination.page_html()
        return render(request, 'consult_record.html', {
            'consult_record': consult_record,
            'page_html': page_html,
            'counter': counter
        })

    def post(self, request):
        pass


class AddEditConsultRecordView(View):
    """
    添加/编辑跟进记录
    """

    def get(self, request, c_id=None):
        c_object = ConsultRecord.objects.filter(pk=c_id).first()
        forms = ConsultRecordModelForm(request, instance=c_object)
        return render(request, 'add_edit_consult_record.html', {'forms': forms})

    def post(self, request, c_id=None):
        c_object = ConsultRecord.objects.filter(pk=c_id).first()
        forms = ConsultRecordModelForm(request, data=request.POST, instance=c_object)
        if forms.is_valid():
            forms.save()
            return redirect('consult_record')
        else:
            return render(request, 'add_edit_consult_record.html', {'forms': forms})


class PaymentView(View):
    def get(self, request):
        return render(request, 'payment.html')


class CountCustomerView(View):
    """
    展示客户成交量统计数据
    """

    def get(self, request):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        week = today - datetime.timedelta(weeks=1)
        month = today - datetime.timedelta(weeks=4)
        condition_dict = {'today': [{'deal_date': today}, {'customers__deal_date': today}],
                          'yesterday': [{'deal_date': yesterday}, {'customers__deal_date': yesterday}],
                          'week': [{'deal_date__gte': week}, {'customers__deal_date__gte': week}],
                          'month': [{'deal_date__gte': month}, {'customers__deal_date__gte': month}]}
        condition = request.GET.get('date', 'today')
        customer_obj = Customer.objects.filter(**condition_dict[condition][0]).order_by('-deal_date')
        u_obj = UserInfo.objects.filter(positions__depart_id=1, **condition_dict[condition][1]).values('username',
                                                                                                       'customers').distinct()
        ret = {}
        for item in u_obj:
            if item['username'] in ret.keys():
                ret[item['username']] += 1
            else:
                ret[item['username']] = 1
        ret = [[k, v] for k, v in ret.items()]
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, customer_obj)
        page_html, customer_obj, counter = pagination.page_html()
        return render(request, 'count_customer.html', {
            'customer_obj': customer_obj,
            'page_html': page_html,
            'counter': counter,
            'ret': ret
        })

    def post(self, request):
        pass
