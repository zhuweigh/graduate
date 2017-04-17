#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect, render_template
from application.base import BaseManager, render_jinja
from application.db import models
from sqlalchemy.sql import and_, or_
import  json
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
from datetime import datetime


render = render_jinja('static/templates/search', encoding='utf-8',)

# def judge_semester(user, semester):
#     now = datetime.now()
#
# class GridS(BaseManager):
#     def get(self):
#         params = request.args
#         print 'sssssssss', params.get("name")
#         filters = {}
#         panger = Pager()
#         page, total_paper, records, rows = panger.grid_rows_query(params=params, table='grade', mode='count')
#         cells = ['id', 'name', 'sex', 'score', 'class_', 'c_type', 'course_id']
#         rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
#         return rows_json

class GradeSearch(BaseManager):

    def get(self):

        semester = []
        course = []
        params = request.args
        number = session.get('username')
        s = params.get('key_semester')

        if s:
            grades = models.Grade.query.filter(and_(models.Grade.number==number,models.Grade.semester==semester)).all()
            c_obj = json.loads(grades[0].detail)
            semester.append(c_obj.semester)
            course.append(c_obj)
            # for key, value in c_obj.iteritems():
            #
            #     if key in ["name", "number"]:
            #         continue
            #     else:
            #         # course_value.append(course)
            #         print key , value

            return  render.search(semester, course=course)
        else:
            grades = models.Grade.query.filter_by(number='2013128712').all()
            print  "------------", grades
            for grade in grades:
                 c_obj = json.loads(grade.detail)
                 semester.append('2013-2014')
                 course.append(c_obj)
            print semester, course

            return render.search(semester=semester, course=course)

app = Blueprint('search_app', __name__, template_folder='templates')
app.add_url_rule('/grade', view_func=GradeSearch.as_view('grade_search'))
# app.add_url_rule('/result', view_func=Result.as_view('grid_search'))