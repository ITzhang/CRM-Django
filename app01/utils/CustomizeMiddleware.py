import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, reverse


# 验证用户是否登录中间件
class AuthUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path
        for url in settings.URL_WHITE_LIST:
            if re.match(url, current_path):
                return None

        if not request.user.is_authenticated:
            return redirect('{}?next={}'.format(reverse('login'), current_path))
