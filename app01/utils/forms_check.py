from re import search
from django import forms
from django.forms import widgets as wid
from app01.models import UserInfo, Customer, ConsultRecord
from django.core.exceptions import ValidationError
from django.urls import reverse


class RegModelForm(forms.ModelForm):
    """
    注册modelform
    """
    confirm_password = forms.CharField(min_length=6,
                                       max_length=16,
                                       label='确认密码',
                                       error_messages={'required': '密码不能为空',
                                                       'min_length': '密码不能少于6位'},
                                       widget=wid.PasswordInput(attrs={'placeholder': "请确认密码"})
                                       )

    class Meta:
        model = UserInfo
        fields = ['username',
                  'password',
                  'confirm_password',
                  'email',
                  'tel',
                  ]
        labels = {
            'username': '用户名',
            'password': '密码',
            'email': '邮箱',
            'tel': '手机号码'
        }
        # 校验失败错误信息
        error_messages = {'username': {'required': '用户名不能为空',
                                       'min_length': '用户名不能少于4位'},
                          'password': {'required': '密码不能为空',
                                       'min_length': '密码不能少于6位'},
                          'email': {"required": "邮箱不能为空", "invalid": "邮箱格式错误"},
                          'tel': {'required': '手机号不能为空'}
                          }
        widgets = {'username': wid.TextInput(attrs={'placeholder': "用户名为4~16为位", 'data-foolish-msg': '用户名不能为空'}),
                   'password': wid.PasswordInput(attrs={'placeholder': "密码为6~16位"}),
                   'email': wid.EmailInput(attrs={'placeholder': "请输入邮箱邮箱"}),
                   'tel': wid.TextInput(attrs={'placeholder': "请输入手机号"}),
                   }

    # 校验用户名是否已存在（局部钩子）
    def clean_username(self):
        val = self.cleaned_data.get('username')
        if UserInfo.objects.filter(username=val).first():
            raise ValidationError('用户名已存在')
        else:
            return val

    # 校验密码不能位纯数字
    def clean_password(self):
        val = self.cleaned_data.get('password')
        if val.isdigit():
            raise ValidationError('密码不能为纯数字')
        else:
            return val

    # 校验邮箱格式
    def clean_email(self):
        val = self.cleaned_data.get('email')
        if search(r'^[\w.\-]+@(?:[a-z0-9]+(?:-[a-z0-9]+)*\.)+[a-z]{2,3}$', val):
            return val
        else:
            raise ValidationError('无效的邮箱')

    # 校验手机号格式
    def clean_telephone(self):
        val = self.cleaned_data.get('tel')
        if search(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', val):
            return val
        else:
            raise ValidationError('无效的手机号')

    # 校验两次密码是否一致（全局钩子）
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data


class CustomerModelForm(forms.ModelForm):
    """
    客户modelform
    """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        position_list = [x['title'] for x in request.user.positions.all().values('title')]
        if request.path == reverse('customer_public_add') or '销售总监' in position_list:
            queryset_consultant = UserInfo.objects.filter(positions__depart__name='销售部').distinct()
            initial = None
        else:
            queryset_consultant = UserInfo.objects.filter(username=request.user.username)
            initial = queryset_consultant.first()
        self.fields['consultant'] = forms.ModelChoiceField(queryset=queryset_consultant,
                                                           initial=initial,
                                                           label='销售', required=False)

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {'name': wid.TextInput(attrs={'class': 'am-input-sm'}),
                   'birthday': wid.DateInput(attrs={'type': 'date'})}


class ConsultRecordModelForm(forms.ModelForm):
    """
    跟进记录modelform
    """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset_customer = Customer.objects.filter(consultant=request.user)
        self.fields['customer'] = forms.ModelChoiceField(queryset=queryset_customer,
                                                         initial=queryset_customer.first(),
                                                         label='所咨询客户')
        queryset_consultant = UserInfo.objects.filter(username=request.user.username)
        self.fields['consultant'] = forms.ModelChoiceField(queryset=queryset_consultant,
                                                           initial=queryset_consultant.first(),
                                                           label='跟进人')

    class Meta:
        model = ConsultRecord
        exclude = ['delete_status']
