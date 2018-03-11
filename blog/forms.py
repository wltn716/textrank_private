# -*- coding: utf-8 -*-
from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.Form):
		fields = ('title', 'text')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.