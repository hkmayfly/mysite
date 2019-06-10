from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from . import models


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名", max_length=20, min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名(长度3~20)'}
        )
    )
    password1 = forms.CharField(label="密码", max_length=18, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': '请输入密码(长度6~18)'}))
    password2 = forms.CharField(label="确认密码", max_length=18, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}))
    email = forms.EmailField(label="邮箱地址",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册邮箱'}))
    captcha = CaptchaField(label='验证码')


    #
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if models.User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('用户名已存在')
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if models.User.objects.filter(username=email).exists():
    #         raise forms.ValidationError('邮箱已存在')
    #     return email
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 != password2:
    #         raise forms.ValidationError('两次密码不一致')
    #     return password2
