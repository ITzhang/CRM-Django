import copy

class Pagination(object):
    def __init__(self, request, current_page_num, data_obj, per_page_num=10, pager_count=11):
        '''
        封装分页相关数据
        :param current_page_num: 当前请求的页码
        :param all_count:       数据库中所有记录的总数
        :param per_page_num:    每页显示的数据条数
        :param pager_count:     最多显示的页码个数
        '''
        # 如果用户请求体中页码为非数字字符则返回第一页的数据
        try:
            current_page_num = int(current_page_num)
        except ValueError:
            current_page_num = 1
        # 请求页码小于1，返回第一页数据
        if current_page_num < 1:
            current_page_num = 1
        self.current_page_num = current_page_num
        self.data_obj = data_obj
        self.all_count = data_obj.count()
        self.per_page_num = per_page_num
        all_pager, tmp = divmod(self.all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager
        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)
        self.request = request

    @property
    def start(self):
        return (self.current_page_num - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page_num * self.per_page_num

    # 给每条记录加上编号
    def insert_obj_num(self):
        self.data_obj = self.data_obj[self.start:self.end]
        page_num = list(range(self.start + 1, self.end + 1))
        for i, el in enumerate(self.data_obj):
            el.page_num = page_num[i]

    # 保留搜索条件
    def get_param(self, page_num):
        url_param = copy.deepcopy(self.request.GET)
        url_param['page'] = page_num
        return url_param.urlencode()

    # 确定页码的起始位置和结束位置
    def page_point(self):
        # 如果总页码<11个
        if self.all_pager <= self.pager_count:
            page_start = 1
            page_end = self.all_pager + 1
        else:
            # 当前页如果<=页面上做多显示11/2个页码
            if self.current_page_num <= self.pager_count_half:
                page_start = 1
                page_end = self.pager_count + 1
            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page_num + self.pager_count_half) > self.all_pager:
                    page_start = self.all_pager - self.pager_count + 1
                    page_end = self.all_pager + 1
                else:
                    page_start = self.current_page_num - self.pager_count_half
                    page_end = self.current_page_num + self.pager_count_half + 1
        return page_end, page_start

    # 生成HTML,返回data数据
    def page_html(self):
        page_end, page_start = self.page_point()
        page_html_list = []

        # 首页
        first_page = '<li><a href="?%s">首页</a></li>' % (self.get_param(1),)
        page_html_list.append(first_page)

        if self.current_page_num <= 1:
            prev_page = '<li class="am-disabled"><a href="#">«</a></li>'
        else:
            prev_page = '<li><a href="?%s">«</a></li>' % (self.get_param(self.current_page_num - 1),)
        page_html_list.append(prev_page)

        for i in range(page_start, page_end):
            if i == self.current_page_num:
                temp = '<li class="am-active"><a href="?%s">%s</a></li>' % (self.get_param(i), i)
            else:
                temp = '<li><a href="?%s">%s</a></li>' % (self.get_param(i), i,)
            page_html_list.append(temp)

        if self.current_page_num >= self.all_pager:
            next_page = '<li class="am-disabled"><a href="#">»</a></li>'
        else:
            next_page = '<li><a href="?%s">»</a></li>' % (self.get_param(self.current_page_num + 1),)
        page_html_list.append(next_page)
        # 尾页
        last_page = '<li><a href="?%s">尾页</a></li>' % (self.get_param(self.all_pager),)
        page_html_list.append(last_page)
        self.insert_obj_num()
        return ''.join(page_html_list), self.data_obj, self.all_count
