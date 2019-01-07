from django.db import models
from app01.models import Position


# Create your models here.

class Menu(models.Model):
    """
    菜单列表标题
    """
    title = models.CharField(max_length=32, verbose_name='菜单')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    menu_id = models.CharField(max_length=32, verbose_name='菜单id名', default='暂无')

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表（二级菜单表）
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=60, verbose_name='权限')
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, null=True, blank=True)
    positions = models.ManyToManyField('app01.Position', verbose_name='职位所拥有的权限', blank=True)
    pid = models.ForeignKey('Menu', related_name='classify', verbose_name='url分类', on_delete=models.CASCADE, null=True,
                            blank=True)
    related_name = models.CharField(max_length=32, verbose_name='别名', null=True,blank=True)

    def __str__(self):
        return self.title
