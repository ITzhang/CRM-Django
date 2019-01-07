import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse
from rbac.models import Permission


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path

        for item in settings.URL_WHITE_LIST:
            if re.match(item, current_path):
                return None

        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        for item in permission_list:
            if re.match(r'^{}$'.format(item['url']), current_path):
                # 给当前请求注入一个父级菜单标记
                request.url_classify = item['url_classify']
                return None
        else:
            return HttpResponse('没有访问权限')
