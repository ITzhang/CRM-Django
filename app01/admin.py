from django.contrib import admin

from app01.models import Customer, Campuses, ClassList, ConsultRecord, Department, Position, UserInfo
from rbac.models import Menu, Permission
from student_manage.models import Student,StudentStudyRecord,ClassStudyRecord


# Register your models here.


class PositionView(admin.ModelAdmin):
    list_display = ['title', 'depart']


class PermissionView(admin.ModelAdmin):
    list_display = ['title', 'url', 'menu', 'pid']
    list_editable = ['url', 'menu', 'pid']


admin.site.register(Customer)
admin.site.register(Campuses)
admin.site.register(ClassList)
admin.site.register(ConsultRecord)
admin.site.register(Department)
admin.site.register(Position, PositionView)
admin.site.register(UserInfo)
admin.site.register(Menu)
admin.site.register(Permission, PermissionView)
admin.site.register(Student)
admin.site.register(ClassStudyRecord)
