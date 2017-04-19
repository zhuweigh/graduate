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

        semester = {}
        course = []
        params = request.args
        # number = session.get('username')
        s = params.get('key_semester')
        name = params.get('key_name')
        number = params.get("key_number")
        print name , number, s
        grades = ''
        if s and number:
            grades = models.Grade.query.filter(and_(models.Grade.number==number,models.Grade.semester==s, )).all()
        elif s and name:
            grades = models.Grade.query.filter(and_(models.Grade.name == name, models.Grade.semester == s, )).all()
        elif name:
            grades = models.Grade.query.filter(models.Grade.name == name).all()
        if grades:
            for grade in grades:
                semester["semester"] = grade.semester
                c_obj = json.loads(grade.detail)
                c_obj.update(semester)
                course.append(c_obj)
                print course
                print  semester

            return render.search_grade(course=course)
        else:
            return render.search_grade()

class UnpassSearch(BaseManager):
    def get(self):
        params = request.args
        semester = {}
        L = []

        name = params.get("key_name")
        number = params.get("key_number")
        s = params.get("key_semester")
        # name = '关东健'
        grades = []
        # gradeobj = models.Grade.query.filter_by(name=name).all()
        if name and s:
            grades = models.Grade.query.filter(and_(models.Grade.name == name, models.Grade.semester == s, )).all()
        elif number and s:
            grades = models.Grade.query.filter(and_(models.Grade.number == number, models.Grade.semester == s, )).all()
        elif name:
            grades = models.Grade.query.filter(and_(models.Grade.name == name)).all()

        for grade in grades:
            semester["semester"] = grade.semester
            c_obj = json.loads(grade.detail)
            c_obj.update(semester)
            for key, value in c_obj.iteritems():
                storage = {}
                # print  key ,value
                if key == 'semester':
                    continue
                score = c_obj[key]['grade']
                if score == '- ':
                    continue
                # print type(score)
                score = int(score)
                if score < 60:
                    storage['course_name'] = key
                    storage['course_type'] = c_obj[key]['type']
                    storage['semester'] = c_obj['semester']
                    storage['grade'] = score
                    storage['course_number'] = c_obj[key]['number']
                L.append(storage)
                print  L
                # print storage

        return  render.search_unpass(Ls=L)

app = Blueprint('search_app', __name__, template_folder='templates')
app.add_url_rule('/grade', view_func=GradeSearch.as_view('grade_search'))
app.add_url_rule('/unpass', view_func=UnpassSearch.as_view('unpass_search'))

# app.add_url_rule('/result', view_func=Result.as_view('grid_search'))