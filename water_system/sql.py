# C:\Bin\environment\python
# -*- coding: utf-8 -*-
# @Time : 2022/11/12 16:51
# @Author : south(南风)
# @File : sql.py
# Describe:
# -*- coding: utf-8 -*-
import os

import pymysql
from matplotlib.font_manager import FontProperties
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar


class Sql:
    def __init__(self):
        self.font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=10)
        self.db = pymysql.connect(user='root', password='root', database='watersystem', charset='utf8')
        self.cursor = self.db.cursor()

    # 购水表前十
    def ten(self, time):
        sql = f"select name,SUM(num) sum from customer_action where MONTH(time)={time}  group by name order by sum DESC limit 10;"
        self.cursor.execute(sql)  # 执行sql语句
        data = self.cursor.fetchall()
        user = []
        num = []
        for i in data:
            user.append(i[0])
            num.append(i[1])
        bar = Bar()
        bar.add_xaxis(user)
        bar.add_yaxis("", num)
        bar.set_global_opts(title_opts=opts.TitleOpts(title="用户前十"))
        a = bar.render("C:\\Users\\south\\Desktop\\Code\\WaterSystem\\templates\\water_system\\render_t.html")
        src = os.path.split(a)[1]
        return src
        # plt.show()

    # 完整的购水表
    def all(self, time):
        sql = f"select name,SUM(num) sum from customer_action where MONTH(time) = {time} group by name order by sum DESC;"
        self.cursor.execute(sql)  # 执行sql语句
        data = self.cursor.fetchall()
        user = []
        num = []
        for i in data:
            user.append(i[0])
            num.append(i[1])

        data = [list(z) for z in zip(user, num)]
        pie = Pie()
        pie.add("", data)
        pie.set_global_opts(title_opts=opts.TitleOpts(title="购水表", pos_top="50"))
        a = pie.render("C:\\Users\\south\\Desktop\\Code\\WaterSystem\\templates\\water_system\\render_a.html")
        src = os.path.split(a)[1]
        return src
        # plt.show()

    # 售卖表
    def water(self, time):
        sql1 = f"select water.type,kS.* from water,(select kind,SUM(num) sum from customer_action where MONTH(time)={time} group by kind) as kS " \
               "where water.wid = kS.kind order by sum DESC "
        self.cursor.execute(sql1)
        data1 = self.cursor.fetchall()
        com = []
        num1 = []
        for j in data1:
            com.append(j[0])
            num1.append(j[2])
        bar = Bar()
        bar.add_xaxis(com)
        bar.add_yaxis("", num1)
        bar.set_global_opts(title_opts=opts.TitleOpts(title="售卖表"))
        a = bar.render("C:\\Users\\south\\Desktop\\Code\\WaterSystem\\templates\\water_system\\render_w.html")
        src = os.path.split(a)[1]
        return src

    # 工作情况
    def work(self, time):
        sql = f"select name,SUM(num) sum from work_action  where MONTH(time)={time} group by name order by sum DESC;"
        self.cursor.execute(sql)  # 执行sql语句
        data = self.cursor.fetchall()
        user = []
        num = []
        for i in data:
            user.append(i[0])
            num.append(i[1])
        data = [list(z) for z in zip(user, num)]
        pie = Pie()
        pie.add("", data)
        pie.set_global_opts(title_opts=opts.TitleOpts(title="工作表"))
        a = pie.render("C:\\Users\\south\\Desktop\\Code\\WaterSystem\\templates\\water_system\\render_wo.html")
        src = os.path.split(a)[1]
        return src


