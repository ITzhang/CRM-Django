import re
from django.template import Library
from django.conf import settings
from django.urls import reverse

register = Library()


@register.inclusion_tag('menu.html')
def show_menu_list(request):
    permission_menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    # 设置当前url的菜单展开
    for menu in permission_menu_dict.values():
        for url in menu['secondary_menu']:
            if request.url_classify == menu['menu_pk']:
                menu['menu_style'] = ['', 'am-in']
                if re.match(r'^{}$'.format(url['url']), request.path):
                    url['url_style'] = 'url-active'
                elif re.match(r'^{}$'.format(url['url']), request.GET.get('next', '')):
                    url['url_style'] = 'url-active'

    return {'permission_menu_dict': permission_menu_dict}


@register.filter
def button_permission(request, url):

    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
