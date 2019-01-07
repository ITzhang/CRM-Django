from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from rbac.models import Permission, Menu
from app01.models import UserInfo, Department, Position
from django.forms.models import modelformset_factory
from rbac.utils.forms_check import PermissionMenuMF, PermissionUrlMF


# Create your views here.

class PermissionPatch(View):
    def get(self, request):
        # 权限数据
        p_list = {}
        menu_list = Menu.objects.all()
        permission_other_list = Permission.objects.filter(pid__isnull=True)
        p_list['其他'] = permission_other_list
        for item in menu_list:
            permission_list = Permission.objects.filter(pid=item)
            p_list[item.title] = permission_list

        # 部门职位数据
        r_list = {}
        depart_list = Department.objects.all()
        for item in depart_list:
            position_list = Position.objects.filter(depart=item)
            r_list[item.name] = position_list

        # 用户数据
        user_list = UserInfo.objects.all()

        # 选中用户角色部门信息
        uid = request.GET.get('uid')
        if uid and uid.isdigit():
            user_positions_list = UserInfo.objects.filter(pk=uid).values('positions')
        else:
            user_positions_list = []
        user_positions_list = [item['positions'] for item in user_positions_list]

        # 选中用户权限信息

        pid = request.GET.get('pid')
        if user_positions_list:
            permission_list = Position.objects.filter(pk__in=user_positions_list).values('permission').distinct()
        elif pid and pid.isdigit():
            permission_list = Position.objects.filter(pk=pid).values('permission').distinct()
        else:
            permission_list = None

        if permission_list:
            permission_list = [item['permission'] for item in permission_list]
        else:
            permission_list = []

        return render(request, 'permission_patch.html',
                      {'p_list': p_list,
                       'r_list': r_list,
                       'user_list': user_list,
                       'user_positions_list': user_positions_list,
                       'permission_list': permission_list,
                       'uid': int(uid) if user_positions_list else None,
                       'pid': int(pid) if pid and permission_list else None
                       })

    def post(self, request):
        if request.POST.get('action') == 'user_position':
            uid = request.POST.get('user_id')
            position_list = request.POST.getlist('position', [])
            user_obj = UserInfo.objects.filter(pk=uid).first()
            user_obj.positions.set(position_list)
        elif request.POST.get('action') == 'position_permission':
            pid = request.POST.get('pid')
            permission_list = request.POST.getlist('permission')
            position_obj = Position.objects.filter(pk=pid).first()
            if position_obj:
                position_obj.permission_set.set(permission_list)

        return redirect(request.get_full_path())


class PermissionMenu(View):

    def get(self, request):
        # 删除菜单
        del_action = request.GET.get('del')
        if del_action:
            Menu.objects.filter(pk=del_action).delete()
            return redirect('rbac:show_permission_menu')
        parms = list(request.GET.values())
        menu_obj = Menu.objects.all()
        model_formset_menu = modelformset_factory(model=Menu, form=PermissionMenuMF, extra=0)
        formset = model_formset_menu(queryset=menu_obj)
        add_forms = PermissionMenuMF()
        return render(request, 'permission_menu.html',
                      {'formset': formset, 'add_forms': add_forms, 'menu_obj': menu_obj, 'parms': parms})

    def post(self, request):
        parms = list(request.GET.values())
        menu_obj = Menu.objects.all()
        action = request.GET.get('action')
        if action == 'add':
            add_forms = PermissionMenuMF(request.POST)
            if add_forms.is_valid():
                add_forms.save()
                return redirect('rbac:show_permission_menu')
            else:
                return render(request, 'permission_menu.html',
                              {'add_forms': add_forms, 'parms': parms, 'menu_obj': menu_obj})
        elif action == 'edit':
            model_formset_menu = modelformset_factory(model=Menu, form=PermissionMenuMF, extra=0)
            formset = model_formset_menu(request.POST)
            if formset.is_valid():
                formset.save()
                return redirect('rbac:show_permission_menu')
            else:
                return render(request, 'permission_menu.html', {'formset': formset, 'parms': parms})


class PermissionUrl(View):
    def get(self, request, mid):
        parms = list(request.GET.values())
        parms_length = len(parms)
        print(parms_length)
        permission_url_list = Permission.objects.filter(pid_id=mid)
        url_formset = modelformset_factory(model=Permission, form=PermissionUrlMF, extra=0)
        formset = url_formset(queryset=permission_url_list)
        add_forms = PermissionUrlMF()
        return render(request, 'permission_url.html', locals())

    def post(self, request, mid):
        parms = list(request.GET.values())
        action = request.GET.get('action')
        if action == 'edit':
            url_formset = modelformset_factory(model=Permission, form=PermissionUrlMF, extra=0)
            formset = url_formset(request.POST)
            if formset.is_valid():
                formset.save()
                return redirect('{}?next={}'.format(request.path, reverse('rbac:show_permission_menu')))
            else:
                return render(request, 'permission_url.html', locals())
        if action == 'add':
            add_forms = PermissionUrlMF(request.POST)
            if add_forms.is_valid():
                add_forms.save()
                return redirect('{}?next={}'.format(request.path, reverse('rbac:show_permission_menu')))
            else:
                return render(request, 'permission_url.html', locals())
