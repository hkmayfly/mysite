from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>', views.blog_detail, name='blog_detail'), # 第几页博客
    path('type/<int:blog_type_id>', views.blogs_with_type, name='blog_with_type'), # 博客类型
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
    # path('daily_pic', views.daily_photo, name='daily_photo'),
]