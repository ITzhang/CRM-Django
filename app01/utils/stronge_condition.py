import copy


def url_parm(request):
    url_parm = copy.deepcopy(request.GET)
    url_parm['next'] = request.path
    url_parm = url_parm.urlencode(safe='/')
