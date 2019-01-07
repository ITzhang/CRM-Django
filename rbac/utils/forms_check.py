from django import forms
from rbac.models import Menu, Permission


class PermissionMenuMF(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'icon', 'menu_id']
        # exclude = ['id']


class PermissionUrlMF(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['title', 'url', 'menu', 'pid', 'related_name']
