# C:\Bin\environment\python
# -*- coding: utf-8 -*-
# @Time : 2022/10/26 14:36
# @Author : south(南风)
# @File : urls.py
# Describe: 
# -*- coding: utf-8 -*-
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('information', views.get_information, name='get_information'),
    path('water1', views.get_water, name='get_water'),
    path('provider', views.get_provider, name='get_provider'),
    path('store', views.get_store, name='get_store'),
    path('buy/', views.buy, name='buy'),
    path('buin/', views.buy_in, name='buin'),
    path('buinr/', views.buy_inr, name='buinr'),
    path('jump', views.jump, name='jump'),
    path('loadout', views.index1, name='loadout'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('myself', views.myself, name='myself'),
    path('edit', views.edit, name='edit'),
    path('rootedit/', views.rootedit, name='rootedit'),
    path('logout', views.user_logout, name='user_logout'),
    path('pic', views.xian, name='xian'),
    path('render_t', views.rens, name='rens'),
    path('render_a', views.rent, name='rent'),
    path('render_w', views.renw, name='renw'),
    path('render_wo', views.renwo, name='renwo'),
    path('out/', views.load, name='out'),
    path('outr/', views.loadr, name='outr'),
    path('delete/', views.delete, name='delete'),
    path('delete1/', views.delete1, name='delete1'),
]



