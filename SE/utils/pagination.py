from SE import models
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    """
        自定义分页组件,使用它需要传入request对象和筛选后的数据
            page: 当前页码
            total_page: 总页码
            filter_ip_content: 筛选后的数据
            page_str: 生成的页码
    """

    def __init__(self, request, filter_ip_content, page_size=15, page_param="page", plus=5, method="GET"):
        """
        :param request: 请求体
        :param filter_ip_content: 筛选后的数据
        :param page_size: 一次展示的总页数
        :param page_param: 前端传递的页码参数
        :param plus: 单边展示的页码数
        """

        # 获取请求体中原本的GET数据
        self.query_dict = copy.deepcopy(request.GET)
        self.query_dict._mutable = True
        print('原查询参数'+self.query_dict.urlencode())

        # 获取前端传递的页码参数
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 获取筛选数据：
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 获取数据库总条数以及筛选后的数据
        total_count = filter_ip_content.count()
        self.filter_ip_content = filter_ip_content[self.start:self.end]

        # 总页码
        total_page, m = divmod(total_count, page_size)
        if m:
            total_page += 1
        self.total_page = total_page

        self.plus = plus

    def html(self):
        # 2. 生成页码
        #   只显示前五页和后五页
        if self.total_page < 2 * self.plus + 1:
            page_start = 1
            page_end = self.total_page + 1
        else:
            if self.page < self.plus + 1:
                page_start = 1
                page_end = 2 * self.plus + 1
            else:
                if self.page + self.plus > self.total_page:
                    page_start = self.total_page - 2 * self.plus + 1
                    page_end = self.total_page + 1
                else:
                    page_start = self.page - self.plus
                    page_end = self.page + self.plus + 1

        page_str_list = []

        # 首页
        self.query_dict[self.page_param] = 1
        first = '<li><a href="?{}"><span aria-hidden="true">首页</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first)

        # 上一页
        if self.page == 1:
            prev = '<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            self.query_dict[self.page_param] = self.page - 1
            prev = '<li><a href="?%s"><span aria-hidden="true">&laquo;</span></a></li>' % (self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(page_start, page_end):
            if i == self.page:
                self.query_dict[self.page_param] = i
                temp = '<li class="active"><a href="?%s">%s</a></li>' % (self.query_dict.urlencode(), i)
            else:
                self.query_dict[self.page_param] = i
                temp = '<li><a href="?%s">%s</a></li>' % (self.query_dict.urlencode(), i)
            page_str_list.append(temp)

        # 下一页
        if self.page == self.total_page:
            after = '<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            self.query_dict[self.page_param] = self.page + 1
            after = '<li><a href="?%s"><span aria-hidden="true">&raquo;</span></a></li>' % (self.query_dict.urlencode())
        page_str_list.append(after)

        # 尾页
        self.query_dict[self.page_param] = self.total_page
        last = '<li><a href="?%s"><span aria-hidden="true">尾页</span></a></li>' % (self.query_dict.urlencode())
        page_str_list.append(last)

        """
        <li><a href="?page=2#">2</a></li
        <li><a href="?page=3">3</a></li>
        <li><a href="?page=4">4</a></li>
        <li><a href="?page=5">5</a></li>
        """

        # 跳转框
        jump = """<li>
                   <form method="get" style="float: left;margin-left: -1px">
                       <input name="page"
                              style="position: relative;float: left;display: inline-block;width: 110px;border-radius:0 "
                              type="number" class="form-control" placeholder="页码">
                       <button id="jump-button" class="btn btn-default" type="submit">跳转</button>
                   </form>
               </li>
               """
        page_str_list.append(jump)

        page_str = mark_safe(''.join(page_str_list))

        print("end of html()"+page_str)

        return page_str
