from django.urls import path, re_path, reverse
from rbac import views

urlpatterns = [
    # 权限分配
    path('permission/patch/', views.PermissionPatch.as_view(), name='permission_patch'),
    path('show_permission_menu/', views.PermissionMenu.as_view(), name='show_permission_menu'),

    # 菜单管理
    re_path(r'^permission_menu/delete/(\d+)$', views.PermissionMenu.as_view(), name='permission_menu_delete'),

    # url管理
    re_path(r'^show_permission_url/(\d+)/$', views.PermissionUrl.as_view(), name='show_permission_url')


]
