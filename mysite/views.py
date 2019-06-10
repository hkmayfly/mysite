from django.shortcuts import render, redirect
from login.views import login_required


# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         message = "所有字段都必须填写！"
#         if username and password:  # 确保用户名和密码都不为空
#             username = username.strip()  # 用户名字符合法性验证
#             # 密码长度验证
#             # 更多的其它验证.....
#             try:
#                 user = models.User.objects.get(name=username)
#                 if user.password == password:
#                     return redirect('/home/')
#                 else:
#                     message = "密码不正确！"
#             except:
#                 message = "用户名不存在！"
#         return render(request, 'login.html', {"message": message})
#     return render(request, 'login.html')
#
#
# def register(request):
#     pass
#     return render(request, 'register.html')
#
#
# def logout(request):
#     pass
#     return redirect('home')
# 比如 这个首页 加上装饰器后  不登录就不能访问 自动跳转到登录页

def home(request):
    return render(request, 'home.html')


def about_me(request):
    return render(request, 'about_me.html')

