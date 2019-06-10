from django.shortcuts import render, redirect, reverse
from . import models
from .forms import UserForm, RegisterForm
import datetime
import hashlib
from django.conf import settings


def my_login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']  # 字典
            password = login_form.cleaned_data['password']
            user = models.User.objects.filter(name=username)[0]
            if user:
                # user = models.User.objects.get(name=username)
                user = models.User.objects.filter(name=username)[0]
                print('用户名%s' % user)
                if not user.has_confirmed:
                    message = '该用户还未经过邮件确认'
                    return render(request, 'login.html', locals())
                if user.password == hash_code(password):
                    # 往session字典写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = "密码不正确！"
            else:
                message = "用户不存在！请先注册！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())

    # return render_to_response('login.html', context)


def register(request):
    # if request.method == 'POST':
    #     reg_form = RegisterForm(request.POST)
    #     if reg_form.is_valid():
    #         username = reg_form.cleaned_data['username']
    #         email = reg_form.cleaned_data['email']
    #         password = reg_form.cleaned_data['password1']
    #         # 创建用户
    #         user = models.User.objects.create(username,email,password)
    #         user.save()
    #         return redirect(request.GET.get('from', reverse('home')))
    # else:
    #     reg_form = RegisterForm()
    #
    # context={}
    # context['reg_form'] = reg_form
    # return render(request, 'register.html', context)
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱已存在，请重新输入！'
                    return render(request, 'register.html', locals())

                # 创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                context = {}
                context['info'] = True
                context['message'] = '注册成功！只差到邮箱激活账户啦，你就能成为我们龙骑士团成员之一啦！╰(*°▽°*)╯'
                context['jump'] = '5秒后自动跳转注册界面'
                return render(request, 'confirm.html', context)
                # 创建成功直接登录状态
                # request.session['is_login'] = True
                # request.session['user_id'] = new_user.id
                # request.session['user_name'] = new_user.name
                # return redirect('/')
                # return redirect('/user/login/')  # 自动跳转到登录页面

        else:
            return render(request, 'register.html', locals())

    register_form = RegisterForm()
    return render(request, 'register.html', locals())


#  return render(request, 'register.html')
# 你想给哪个视图让登陆后才能访问  就在上面加个装饰器


def my_logout(request):
    request.session['is_login'] = False
    del request.session['user_id']
    del request.session['user_name']
    return redirect(reverse('login'))


def login_required(func):
    def inner(request, *args, **kwargs):
        if not request.session.get('is_login'):
            return redirect(reverse('login'))
        else:
            return func(request, *args, **kwargs)

    return inner
    # def logout(request):
    #     if not request.session.get('is_login', None):
    #         # 如果本来就未登录，也就没有登出一说
    #         return redirect("/")
    #     request.session.flush()
    #     # 或者使用下面的方法
    #     # del request.session['is_login']
    #     # del request.session['user_id']
    #     # del request.session['user_name']
    #     return redirect("/")


def hash_code(s, salt='hkmayfly'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '验证电子邮件地址'

    text_content = '''感谢注册hkmayfly.com，您的浏览器不支持网页代码，请联系博主手动激活：tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=1024593536'''

    html_content = '''
                    <p>点击<a href="http://{}/user/confirm/?code={}" target=blank>hkmayfly.com</a>加入318龙骑团大家庭</p>
                    <p style="color:red"><b>注意:</b>此链接{}天内有效，请及时注册！</p>
                    <p>有疑惑请联系博主：<a target="_blank" href="tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=1024593536" target="_blank""><img border="0" src="http://wpa.qq.com/pa?p=1:10245935:13" alt="QQ：1024593536" title="有事您Q我"></a></p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    context = {}
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        context['message'] = '无效的确认请求!'
        context['jump'] = '5秒后自动跳转注册界面'
        context['info'] = False
        return render(request, 'confirm.html', context)

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        context['message'] = '邮件已经过期！请重新注册!'
        context['jump'] = '5秒后自动跳转注册界面'
        context['info'] = False
        return render(request, 'confirm.html', context)
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        context['message'] = '账户已激活！请使用账户登录！'
        context['jump'] = '5秒后自动跳转注册界面'
        context['info'] = True
        return render(request, 'confirm.html', context)
