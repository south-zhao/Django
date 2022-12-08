import os
import time
from datetime import datetime
from threading import Thread

import numpy as np
import pymysql
import xlrd
import xlwt
from django.core.paginator import PageNotAnInteger, InvalidPage, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import authenticate, logout
import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
# Create your views here.
from django.urls import reverse
from matplotlib.font_manager import FontProperties

from WaterSystem import settings
from .sql import Sql
from . import models
from .models import Customer, Water, User, Provider, RootS, AddrArea, WorkAction, CustomerAction, StoreHouse

user = None

rt = None


def checklogin(func):
    def wrapper(request, *args, **kwargs):
        if user or rt:
            return func(request, *args, **kwargs)
        else:
            return redirect("/jump")

    return wrapper


def index(request):
    global user, rt
    water = Water.objects.all()
    if user is None and rt is None:
        return render(request, 'water_system/index.html', {'user1': None, "rt": None, "root": False, 'water': water})
    elif user and rt is None:
        return render(request, 'water_system/index.html', {'user1': user, "rt": None, "root": False, 'water': water})
    elif user is None and rt:
        return render(request, 'water_system/index.html', {'user1': user, "rt": rt, "root": True, 'water': water})


def jump(request):
    return render(request, 'water_system/jump.html', {"msg": True})


def get_provider(request):
    provider = Provider.objects.all()
    if user and rt is None:
        return render(request, 'water_system/provider.html',
                      {'user1': user, "rt": None, "root": False, 'provider': provider})
    elif user is None and rt:
        return render(request, 'water_system/provider.html',
                      {'user1': None, "rt": rt, "root": True, 'provider': provider})
    else:
        return render(request, 'water_system/provider.html',
                      {'user1': user, "rt": rt, "root": False, 'provider': provider})


def get_store(request):
    store = models.StoreHouse.objects.all()
    if user and rt is None:
        return render(request, 'water_system/store.html', {'user1': user, "rt": None, "root": False, 'store': store})
    elif user is None and rt:
        return render(request, 'water_system/store.html', {'user1': None, "rt": rt, "root": True, 'store': store})
    else:
        return render(request, 'water_system/store.html', {'user1': user, "rt": rt, "root": False, 'store': store})


def get_information(request):
    information = Customer.objects.all()
    return render(request, 'water_system/information.html',
                  {'user1': user, "rt": rt, "root": True, 'information': information})


# @checklogin
def get_water(request):
    water = Water.objects.all()
    if user and rt is None:
        return render(request, 'water_system/water.html', {'user1': user, "rt": rt, "root": False, 'water': water})
    elif user is None and rt:
        return render(request, 'water_system/water.html', {'user1': user, "rt": rt, "root": True, 'water': water})
    else:
        return render(request, 'water_system/water.html', {'user1': user, "rt": rt, "root": False, 'water': water})


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        user_1 = models.User.objects.filter(username=username)
        if user_1:
            error = '用户名已经存在'
            return render(request, 'water_system/register.html', {'error': error})
        else:
            if password1 == password:
                user_1 = User()
                user_1.username = username
                user_1.password = password
                user_1.save()
                return render(request, 'water_system/register.html', {'msg': '注册成功'})
    return render(request, 'water_system/register.html')


def login(request):
    water = Water.objects.all()
    if request.method == "POST":
        global user, rt
        username = request.POST.get('username')
        password = request.POST.get('password')
        check = request.POST.get('us')
        if check == "普通用户":
            user = User.objects.get(username=username)
            if user.password == password:
                return render(request, 'water_system/index.html',
                              {'user1': user, "rt": None, "root": False, 'water': water})
            else:
                return HttpResponse("登陆失败")
        else:
            rt = RootS.objects.get(username=username)
            if rt.password == password:
                return render(request, 'water_system/index.html',
                              {'user1': None, "rt": rt, "root": True, 'water': water})
            else:
                return HttpResponse('登录失败')
    return render(request, 'water_system/login.html')


def myself(request):
    global user
    user2 = Customer.objects.get(name=user.username)
    return render(request, "water_system/myself.html", {'user1': user, "root": False, "rt": None, "user2": user2})


# @checklogin
def edit(request):
    global user
    # user1 = models.Customer.objects.filter(name=user.username)
    water = Water.objects.all()
    area = AddrArea.objects.all()
    user2 = Customer.objects.get(name=user.username)
    if request.method == "POST":
        tele = request.POST.get('tele')
        addr1 = request.POST.get('typea')
        addr = request.POST.get('addr')
        addr = addr1 + addr
        wid = request.POST.get('type')
        wo = AddrArea.objects.get(addr=addr1)
        if user2:
            models.Customer.objects.filter(name=user.username).update(tele=tele, addr=addr, wid=wid, work_id=wo.area)
            # user2 = Customer.objects.get(name=user.username)
            return render(request, 'water_system/index.html',
                          {'user1': user, "rt": None, "root": False, 'water': water})
            # return redirect('index')
    return render(request, 'water_system/edit.html', {'user1': user2, 'water': water, 'area': area})


def rootedit(request):
    edit_id = request.GET.get('user_id')
    edit_obj = models.Customer.objects.filter(cid=edit_id).first()
    if request.method == 'POST':
        password = request.POST.get('password')
        tele = request.POST.get('tele')
        addr = request.POST.get('addr')
        num = request.POST.get('num')
        wid = request.POST.get('wid')
        work_id = request.POST.get('work_id')
        models.User.objects.filter(username=edit_obj.name).update(password=password)
        models.Customer.objects.filter(cid=edit_id).update(tele=tele, addr=addr, num=num, wid=wid, work_id=work_id)
        return redirect('/information')
    return render(request, 'water_system/rootedit.html', {"edit_obj": edit_obj})


# 购买
@checklogin
def buy(request):
    global user
    user2 = models.Customer.objects.filter(name=user.username).first()
    water = Water.objects.all()
    w_id = request.GET.get('wid')
    if request.method == "POST":
        wid = request.POST.get('type')
        num = request.POST.get('num')
        if user2:
            models.Customer.objects.filter(name=user.username).update(wid=wid, num=num)
            return render(request, 'water_system/index.html',
                          {'user1': user, "rt": None, "root": False, "m": True, 'water': water})
            # return redirect('index')
    return render(request, 'water_system/buy.html',
                  {"water": water, "w_id": int(w_id), 'user1': user, "rt": None, "root": False})


@checklogin
def buy_in(request):
    global user
    user1 = models.User.objects.filter(username=user.username).first()
    root = False
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT MONTH(time) FROM work_action")
    ase = cursor.fetchall()
    cursor.execute("SELECT DISTINCT YEAR(time) FROM work_action")
    ye = cursor.fetchall()
    cursor.execute("SELECT wid, type FROM water")
    water = cursor.fetchall()
    water1 = []
    for i in water:
        li = [int(i[0]), i[1]]
        water1.append(li)
    ase = [i[0] for i in ase]
    ye = [i[0] for i in ye]
    infe = WorkAction.objects.filter(c_name=user.username)
    paginator = Paginator(infe, 10)
    num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
    page = paginator.page(int(num_p))
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    typ = int(request.GET.get('typ'))
    if year == 0 and month == 0 and typ == 0:
        return render(request, 'water_system/buin.html', locals())
    else:
        if year == 0 and month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        elif month == 0 and typ == 0:
            infe = [i for i in infe if i.time.year == year]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        elif year == 0 and typ == 0:
            infe = [i for i in infe if i.time.month == month]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        elif year == 0:
            infe = [i for i in infe if i.time.month == month and i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        elif month == 0:
            infe = [i for i in infe if i.time.year == year and i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        elif typ == 0:
            infe = [i for i in infe if i.time.year == year and i.time.month == month]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
        else:
            infe = [i for i in infe if i.time.year == year and i.time.month == month and i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buin.html', locals())
    # return render(request, 'water_system/buin.html', locals())


def load(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="result.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Menu')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    colums = ['姓名', '数量', '种类', '种类编号', '花费（/元）', '送水员', '电话', '时间']
    for col in range(len(colums)):
        ws.write(row_num, col, colums[col], font_style)

    font_style = xlwt.XFStyle()
    rows = []
    infe = WorkAction.objects.filter(c_name=user.username)
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    typ = int(request.GET.get('typ'))

    if year == 0 and month == 0 and typ == 0:
        for i in infe:
            li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                  i.time.strftime("%Y-%m-%d %H:%M:%S")]
            rows.append(li)
        for i in rows:
            row_num += 1
            for col in range(len(i)):
                ws.write(row_num, col, i[col], font_style)
        wb.save(response)
        return response
    else:
        if year == 0 and month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ]

            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif month == 0 and typ == 0:
            infe = [i for i in infe if i.time.year == year]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)

            wb.save(response)
            return response
        elif year == 0 and typ == 0:
            infe = [i for i in infe if i.time.month == month]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)

            wb.save(response)
            return response
        elif year == 0:
            infe = [i for i in infe if i.time.month == month and i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)

            wb.save(response)
            return response
        elif month == 0:
            infe = [i for i in infe if i.time.year == year and i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)

            wb.save(response)
            return response
        elif typ == 0:
            infe = [i for i in infe if i.time.year == year and i.time.month == month]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)

            wb.save(response)
            return response
        else:
            infe = [i for i in infe if i.time.year == year and i.time.month == month and i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)
            return response


# 用户退出
def user_logout(request):
    global user, rt
    # response = render(request, 'water_system/index.html')
    # request.session.flush()
    # return response
    if 'username' in request.session:
        del request.session['username']
    resp = redirect('index')
    # 删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    user = None
    rt = None
    return resp


def xian(request):
    global user, rt
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT MONTH(time) FROM work_action")
    ase = cursor.fetchall()
    ase = [i[0] for i in ase]
    today = datetime.today()
    mon = today.month
    sql = Sql()
    src = sql.all(mon).strip('.html')
    src1 = sql.ten(mon).strip('.html')
    src2 = sql.water(mon).strip('.html')
    src3 = sql.work(mon).strip('.html')
    if request.method == "POST":
        time = int(request.POST.get('time'))
        src = sql.all(time).strip('.html')
        src1 = sql.ten(time).strip('.html')
        src2 = sql.water(time).strip('.html')
        src3 = sql.work(time).strip('.html')
        return render(request, 'water_system/pic.html',
                      {'user1': None, "rt": rt, "root": True, "ase": ase, "src": src, "src1": src1, "src2": src2,
                       "src3": src3, "time": time, "msg": True})
    return render(request, 'water_system/pic.html',
                  {'user1': None, "rt": rt, "root": True, "ase": ase, "src": src, "src1": src1, "src2": src2,
                   "src3": src3, "time": mon, "msg": False})


def rens(request):
    return render(request, 'water_system/render_t.html')


def rent(request):
    return render(request, 'water_system/render_a.html')


def renw(request):
    return render(request, 'water_system/render_w.html')


def renwo(request):
    return render(request, 'water_system/render_wo.html')


def buy_inr(request):
    global rt
    rt = models.RootS.objects.filter(username=rt.username).first()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT MONTH(time) FROM work_action")
    ase = cursor.fetchall()
    cursor.execute("SELECT DISTINCT YEAR(time) FROM work_action")
    ye = cursor.fetchall()
    cursor.execute("SELECT cid,name FROM customer")
    na = cursor.fetchall()
    na1 = []
    for i in na:
        li = [int(i[0]), i[1]]
        na1.append(li)
    print(na)
    cursor.execute("SELECT wid, type FROM water")
    water = cursor.fetchall()
    water1 = []
    for i in water:
        li = [int(i[0]), i[1]]
        water1.append(li)
    ase = [i[0] for i in ase]
    ye = [i[0] for i in ye]
    infe = models.WorkAction.objects.all()
    paginator = Paginator(infe, 10)
    num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
    page = paginator.page(int(num_p))
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    typ = int(request.GET.get('typ'))
    us = int(request.GET.get('us'))
    if year == 0 and month == 0 and typ == 0 and us == 0:
        return render(request, 'water_system/buinr.html',
                      {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                       'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
    else:
        if year == 0 and month == 0 and us == 0:
            infe = [i for i in infe if i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif month == 0 and typ == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif year == 0 and typ == 0 and us == 0:
            infe = [i for i in infe if i.time.month == month]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif year == 0 and typ == 0 and typ == 0:
            infe = [i for i in infe if i.c_id == us]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif year == 0 and us == 0:
            infe = [i for i in infe if i.time.month == month and i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif month == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year and i.record.kind.wid == typ]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif typ == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year and i.time.month == month]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif year == 0 and typ == 0:
            infe = [i for i in infe if i.time.month == month and i.c_id == us]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})
        elif year == 0 and month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        elif typ == 0 and month == 0:
            infe = [i for i in infe if i.time.year == year and i.c_id == us]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        elif year == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us and i.time.month == month]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        elif month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us and i.time.year == year]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        elif typ == 0:
            infe = [i for i in infe if i.time.month == month and i.c_id == us and i.time.year == year]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        elif us == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.time.month == month and i.time.year == year]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1,
                           'year': year, 'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us,
                           'na': na1})
        else:
            infe = [i for i in infe if
                    i.time.year == year and i.time.month == month and i.record.kind.wid == typ and i.c_id == us]
            paginator = Paginator(infe, 10)
            num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
            page = paginator.page(int(num_p))
            return render(request, 'water_system/buinr.html',
                          {'user1': None, 'rt': rt, 'root': True, 'ase': ase, 'ye': ye, 'water1': water1, 'year': year,
                           'month': month, 'typ': typ, 'page': page, 'paginator': paginator, 'us': us, 'na': na1})


def loadr(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="result.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Menu')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    colums = ['姓名', '数量', '种类', '种类编号', '花费（/元）', '送水员', '电话', '时间']
    for col in range(len(colums)):
        ws.write(row_num, col, colums[col], font_style)

    font_style = xlwt.XFStyle()
    rows = []
    infe = WorkAction.objects.all()
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    typ = int(request.GET.get('typ'))
    us = int(request.GET.get('us'))
    if year == 0 and month == 0 and typ == 0 and us == 0:
        for i in infe:
            li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                  i.time.strftime("%Y-%m-%d %H:%M:%S")]
            rows.append(li)
        for i in rows:
            row_num += 1
            for col in range(len(i)):
                ws.write(row_num, col, i[col], font_style)
        wb.save(response)
        return response
    else:
        if year == 0 and month == 0 and us == 0:
            infe = [i for i in infe if i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif month == 0 and typ == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0 and typ == 0 and us == 0:
            infe = [i for i in infe if i.time.month == month]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0 and typ == 0 and typ == 0:
            infe = [i for i in infe if i.c_id == us]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0 and us == 0:
            infe = [i for i in infe if i.time.month == month and i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif month == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year and i.record.kind.wid == typ]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif typ == 0 and us == 0:
            infe = [i for i in infe if i.time.year == year and i.time.month == month]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0 and typ == 0:
            infe = [i for i in infe if i.time.month == month and i.c_id == us]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0 and month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif typ == 0 and month == 0:
            infe = [i for i in infe if i.time.year == year and i.c_id == us]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif year == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us and i.time.month == month]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif month == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.c_id == us and i.time.year == year]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif typ == 0:
            infe = [i for i in infe if i.time.month == month and i.c_id == us and i.time.year == year]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        elif us == 0:
            infe = [i for i in infe if i.record.kind.wid == typ and i.time.month == month and i.time.year == year]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response
        else:
            infe = [i for i in infe if
                    i.time.year == year and i.time.month == month and i.record.kind.wid == typ and i.c_id == us]
            for i in infe:
                li = [i.c_name, i.num, i.record.kind.type, i.record.kind.wid, i.record.money, i.name, i.tele,
                      i.time.strftime("%Y-%m-%d %H:%M:%S")]
                rows.append(li)
            for i in rows:
                row_num += 1
                for col in range(len(i)):
                    ws.write(row_num, col, i[col], font_style)
            wb.save(response)

            return response


def delete(request):
    edit_id = request.GET.get('user_id')
    edit_obj = models.Customer.objects.filter(cid=edit_id).first()

    a = User.objects.filter(username=edit_obj.name)

    edit_obj.delete()

    a.delete()
    information = Customer.objects.all()
    return render(request, 'water_system/information.html',
                  {'user1': user, "rt": rt, "root": True, 'information': information})


def delete(request):
    edit_name = request.GET.get('user_name')
    edit_obj = models.Customer.objects.filter(name=edit_name).first()
    a = User.objects.filter(username=edit_obj.name)
    water = Water.objects.all()
    edit_obj.delete()
    a.delete()
    global user
    user = None
    return render(request, 'water_system/index.html', {'user1': None, "rt": None, "root": False, 'water': water})


def wrdb(sheet):
    rows = sheet.nrows
    for i in range(1, rows):
        rows_value = sheet.row_values(i)
        models.Provider.objects.filter(name=rows_value[0]).update(supply=rows_value[1])


def index1(request):
    global user
    water = Water.objects.all()
    if request.method == "POST":
        file = request.FILES.get('file')
        # 创建upload文件夹
        if not os.path.exists(settings.UPLOAD_ROOT):
            os.makedirs(settings.UPLOAD_ROOT)
        try:
            if file is None:
                return HttpResponse('请选择要上传的文件')
            file_path = os.path.join(settings.UPLOAD_ROOT, file.name)
            print(file_path)
            # 循环二进制写入
            with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
                for i in file.readlines():
                    f.write(i)
            # 写入 mysql
            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheets()[0]
            rows = sheet.nrows
            thread = Thread(target=wrdb, args=(sheet,))
            thread.start()
            return render(request, 'water_system/index.html', {'user1': user, "rt": rt, "root": True, "l": True, "water": water})
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'water_system/upload.html', {'user1': user, "rt": rt, "root": True})
