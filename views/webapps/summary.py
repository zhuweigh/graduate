#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
from search import GradeList,Unpass
from calculation import  Clculation
import json
import numpy as np
import matplotlib.pyplot as plt

from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/summary', encoding='utf-8',)

class SummaryAll(BaseManager):
    def get(self):
        # print "------------------------"
        return render.summary_all()
    def post(self):
        params = request.form
        class_ = params.get("class_")
        semester = params.get("semester")
        flag = params.get("flag")
        print class_, semester, flag
        if flag:
            if flag == "unpass":
                obj = Unpass(class_, semester)
                result = obj.get_unpass()
                if result:
                    print result
                return 'ok'
            elif flag == "point":


                obj = Clculation(class_, semester)
                result = obj.deal_cal()
                # print result
                if result:
                    low = []
                    middle = []
                    high = []
                    for r in result:

                        if float(r['point']) < int(1.3):
                            low.append(r)
                        elif float(r['point']) > int(1.3) and  float(r['point']) < int(3):
                            middle.append(r)
                        else:
                            high.append(r)
                    plt.rcParams['font.sans-serif'] = ['SimHei']
                    bar_x = []

                return  'ok'
        else:
            return render.summary_all()

app = Blueprint('summary_app', __name__, template_folder='templates')
app.add_url_rule('/show', view_func=SummaryAll.as_view('summary_lists'))