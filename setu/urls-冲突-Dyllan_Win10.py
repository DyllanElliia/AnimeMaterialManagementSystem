"""setu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect


def TEXT(request):
    #print('u: ')
    u=""
    if request.POST:
        u=request.POST['USER']
        p=request.POST['PWD']
    #state_str='密码正确，正在登陆系统...'
    state_str='用户名或者密码有误(⊙︿⊙)'
    return render(request,'New_login.html',{"state":state_str})

from function import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),
    path('register/',register),
]
