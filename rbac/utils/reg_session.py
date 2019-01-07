from app01.models import Position
from django.conf import settings


def initial_session(user, request):
    """
    将当前登录用户的所有权限注入到session
    :param user: 当前登录用户
    :param request:
    :return:
    """
    permissions = Position.objects.filter(userinfo=user).values('permission__url',
                                                                'permission__title',
                                                                'permission__menu__icon',
                                                                'permission__menu__pk',
                                                                'permission__menu__title',
                                                                'permission__menu__menu_id',
                                                                'permission__pid_id').distinct()

    permissions = permissions
    permission_list = []
    permission__menu_dict = dict()
    for item in permissions:
        # 权限列表
        permission_list.append({
            'url': item['permission__url'],
            'url_classify': item['permission__pid_id']
        })

        # 菜单列表
        menu_pk = item['permission__menu__pk']

        # 没有菜单列表的权限
        if item['permission__menu__pk']:
            if menu_pk not in permission__menu_dict:
                permission__menu_dict[menu_pk] = {
                    'menu_title': item['permission__menu__title'],
                    'menu_icon': item['permission__menu__icon'],
                    'menu_id': item['permission__menu__menu_id'],
                    'menu_pk': item['permission__menu__pk'],

                    # menu class名称
                    'menu_style': ['am-collapsed', ''],
                    'secondary_menu': [
                        {
                            'title': item['permission__title'],
                            'url': item['permission__url'],
                            'url_style': '',
                        }
                    ]
                }
            else:
                permission__menu_dict[menu_pk]['secondary_menu'].append(
                    {
                        'title': item['permission__title'],
                        'url': item['permission__url']
                    }
                )
    # 将当前登录用户的权限列表注入session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # 将当前登录用户的菜单列表注入session
    request.session[settings.MENU_SESSION_KEY] = permission__menu_dict
