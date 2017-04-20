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



class GradeList:
    def __init__(self, class_, name, s, number):
        self.class_ = class_
        self.name = name
        self.s = s
        self.number = number

    def deal_grade_show(self):

        grades = ''
        c_obj = ''
        if self.class_:
            course = []
            if self.class_ and self.s:
                grades = models.Grade.query.filter(and_(models.Grade.class_ == self.class_, models.Grade.semester == self.s)).all()
            else:
                return "wrong", None, None

            for grade in grades:
                c_obj = json.loads(grade.detail)
                # c_obj["name"] = grade.name
                c_obj["semester"] = grade.semester
                c_obj['name'] = grade.name
                c_obj['number'] =grade.number
                c_obj['class_'] =grade.class_
                # c_obj["class_"] =grade.class_
                course.append(c_obj)
                # print "--------------",course

            return course, c_obj, None
        elif self.name:
            semester = {}
            course = []
            if self.name and self.s:
                grades = models.Grade.query.filter(and_(models.Grade.semester == self.s, models.Grade.name == self.name)).all()

            elif self.name:
                grades = models.Grade.query.filter(models.Grade.name == self.name).all()

            for grade in grades:
                semester["semester"] = grade.semester
                c_obj = json.loads(grade.detail)
                c_obj.update(semester)
                course.append(c_obj)

            return course, None, None

        elif self.s and self.number:
            semester = {}
            course = []
            grades = models.Grade.query.filter(and_(models.Grade.semester == self.s, models.Grade.number == self.number)).all()
            for grade in grades:
                semester["semester"] = grade.semester
                c_obj = json.loads(grade.detail)
                c_obj.update(semester)
                course.append(c_obj)
            return course,None, None
        else:
            return None,None, None

class GradeSearch(BaseManager):

    def get(self):

        params = request.args
        s = params.get('key_semester')
        name = params.get('key_name')
        number = params.get("key_number")
        class_ = params.get("key_class")
        print name , number, s, class_
        obj = GradeList(class_, name, s, number)
        k, v, n = obj.deal_grade_show()
        if k and v:
            print "kjjjjjjj"
            return render.search_grade(grades=k, courses=v)
        elif k:
            return render.search_grade(course=k)
        else:
            return  render.search_grade()



class Unpass:
    def __init__(self, class_=None, s=None, name=None, number=None):
        self.class_ = class_
        self.s = s
        self.name = name
        self.number = number
        self.L =[]

    def get_unpass(self):
        grades = ''

        semester = {}
        if self.class_ and self.s:
            grades = models.Grade.query.filter(and_(models.Grade.class_ == self.class_, models.Grade.semester == self.s)).all()
        elif self.name and self.s:
            grades = models.Grade.query.filter(and_(models.Grade.name == self.name, models.Grade.semester == self.s, )).all()
        elif self.number and self.s:
            grades = models.Grade.query.filter(and_(models.Grade.number == self.number, models.Grade.semester == self.s, )).all()
        elif self.name:
            grades = models.Grade.query.filter(and_(models.Grade.name == self.name)).all()
        elif self.class_:
            grades = models.Grade.query.filter(and_(models.Grade.class_ == self.class_)).all()

        for grade in grades:
            semester["semester"] = grade.semester
            semester["name"] = grade.name
            c_obj = json.loads(grade.detail)
            c_obj.update(semester)
            for key, value in c_obj.iteritems():
                storage = {}

                if key in ['semester', 'name']:
                    continue
                score = int(c_obj[key]['grade'])
                if score == 0:
                    continue
                # print type(score)
                score = int(score)
                if score < 60:
                    storage['course_name'] = key
                    storage['course_type'] = c_obj[key]['type']
                    storage['semester'] = c_obj['semester']
                    storage['grade'] = score
                    storage['name'] = c_obj['name']
                    storage['course_number'] = c_obj[key]['number']
                    self.L.append(storage)
        # print  "-----------------",self.L     # print  L
        return  self.L


class UnpassSearch(BaseManager):
    def get(self):
        params = request.args

        class_ = params.get("key_class")
        name = params.get("key_name")
        number = params.get("key_number")
        s = params.get("key_semester")

        obj = Unpass(class_, s, name, number)
        L = obj.get_unpass()
        if L:
            return render.search_unpass(Ls=L)
        else:
            return  render.search_unpass()
app = Blueprint('search_app', __name__, template_folder='templates')
app.add_url_rule('/grade', view_func=GradeSearch.as_view('grade_search'))
app.add_url_rule('/unpass', view_func=UnpassSearch.as_view('unpass_search'))

# app.add_url_rule('/result', view_func=Result.as_view('grid_search'))