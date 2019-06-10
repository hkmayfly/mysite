from django.shortcuts import render_to_response, get_object_or_404, render
from .models import Blog, BlogType
from django.core.paginator import Paginator  # 分页器
from django.conf import settings  # 引用全局设置变量
from django.db.models import Count
from login.views import login_required

import requests
from urllib.parse import urlencode
import os
from multiprocessing.pool import Pool
import re


def same_code(request, blogs_all_list):
    # 分页
    paginator = Paginator(blogs_all_list, settings.ARTICLE_OF_PAGE_NUM)  # 每十篇分一页
    page_num = request.GET.get('page', 1)  # GET请求获取页面参数
    page_of_blogs = paginator.get_page(page_num)
    current_page = page_of_blogs.number  # 获取当前页面
    # 处理页码范围问题
    page_range = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    # 判断页码是否跳页，加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 判断第一个是否为“1”页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    # 判断最后一个是否为最大页码
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类中的博客数量
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    # 获取日期归档对应日期的博客数量
    blog_dates = Blog.objects.dates('pub_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(pub_time__year=blog_date.year, pub_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 博客分页返回
    # context['blog_types'] = blog_types_list
    # 使用annotate拓展查询字段
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # context['blogs_count'] = Blog.objects.all().count()
    # 获取时间
    # context['blog_dates'] = Blog.objects.dates('pub_time', 'month', order='DESC')
    context['blog_dates'] = blog_dates_dict
    return context


@login_required
def blog_list(request):  # 博客列表
    # 分页
    blogs_all_list = Blog.objects.all()
    context = same_code(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


@login_required
def blog_detail(request, blog_id):  # 博客详细
    blog = get_object_or_404(Blog, pk=blog_id)
    Blog.increase_reader_num(blog)
    context = {}
    context['blog'] = blog
    # 上一篇博客：先获取前面全部，再获取最后一篇
    context['previous_blog'] = Blog.objects.filter(pub_time__gt=blog.pub_time).last()
    # 下一篇博客：先获取后面全部，再获取第一篇
    context['next_blog'] = Blog.objects.filter(pub_time__lt=blog.pub_time).first()
    return render(request, 'blog_detail.html', context)


@login_required
def blogs_with_type(request, blog_type_id):  # 标签页面
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    # 分页
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = same_code(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


@login_required
def blogs_with_date(request, year, month):
    # 获取日期归档对应日期的博客数量
    blog_dates = Blog.objects.dates('pub_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(pub_time__year=blog_date.year, pub_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    # 找到具体年月的文章
    blogs_all_list = Blog.objects.filter(pub_time__year=year, pub_time__month=month)
    # 分页
    context = same_code(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    context['blog_dates'] = Blog.objects.dates('pub_time', 'month', order='DESC')
    context['blog_dates'] = blog_dates_dict

    return render(request, 'blog_with_date.html', context)


# def daily_photo(request):  # 爬虫
#     class Glob:
#         def __init__(self):
#             self.i = 1
#
#     GL = Glob()
#
#     headers = {
#         'Host': 'wall.alphacoders.com',
#         'Referer': 'https://wall.alphacoders.com/by_favorites.php?quickload=807801&page=1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
#         'X-Requested-With': 'XMLHttpRequest'
#     }
#
#     def get_page(page):
#         params = {
#             # 'search':'fantasy+tiger',
#             'quickload': '807801',
#             'page': page,
#         }
#         base_url = 'https://wall.alphacoders.com/featured.php?'
#         url = base_url + urlencode(params)
#         try:
#             resp = requests.get(url, headers=headers)
#             print(url)
#             # print('ok')
#             if resp.status_code == 200:
#                 return resp.text
#         except requests.ConnectionError:
#             print('no1')
#             return None
#
#     def get_imageurl(html):
#         result = re.findall('[a-zA-z]+://images+[^\s]+jpg', html)
#         return result
#
#     def main(page):
#         GL.i = 0
#         html = get_page(page)
#         result = get_imageurl(html)
#         file_name = 'D:\\Project\\Myblog\\mysite\\blog\\static' + os.path.sep + str(page) + '页'
#         if not os.path.exists(file_name):
#             os.makedirs(file_name)
#         # if not os.path.exists(file_path):
#         # os.makedirs(file_path)
#         for url in result:
#             with open(file_name + os.path.sep + str(page) + '-' + str(GL.i) + '.jpg', 'wb') as f:
#                 content = re.sub('-+[3-4]\d{2}-', '-1920-', url)
#                 print(content)
#                 image = requests.get(content)
#                 f.write(image.content)
#                 # time.sleep(1)
#                 GL.i += 1
#
#     if __name__ == '__main__':
#         pool = Pool()
#         Scope = ([i for i in range(1, 31)])
#         pool.map(main, Scope)
#         pool.close()
#         pool.join()
#
#     return render(request, 'daily_photo.html')
