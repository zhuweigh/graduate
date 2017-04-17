#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
import  os
from xlrd import open_workbook
from collections import OrderedDict
from application.apps import app as app_
import  json
render = render_jinja('static/templates/grade', encoding='utf-8',)
UPLOAD_FOLDER = '/root/desigine/studentinfomanager/application/static/upload'

data = open_workbook(os.path.join(UPLOAD_FOLDER, "grade.xls"))
table = data.sheets()[0]
course = {}
info = {}

class DealTable(object):
    def __init__(self, p_col_start=None, p_col_end=None, p_row_start=None, p_row_end=None,
                 college=None, subject=None, class_=None):

        self.p_col_start = p_col_start
        self.p_col_end = p_col_end
        self.p_row_start = p_row_start
        self.p_row_end = p_row_end
        self.college = college
        self.subject = subject
        self.class_ = class_
    def deal_score(self):
        # print course
        for row in range(self.p_row_start, self.p_row_end):
            for col in range(self.p_col_start, self.p_col_end):

                if not table.row_values(row)[col]:
                    continue
                else:
                    subd = course[table.col_values(col)[0]] = {}
                    # print course
                    subd['number'] = table.row_values(self.p_row_start - 4)[col]
                    subd['type'] = table.row_values(self.p_row_start - 3)[col]
                    subd['score'] = table.row_values(self.p_row_start - 2)[col]
                    course[table.col_values(col)[0]]['grade'] = table.row_values(row)[col]
                    # info['number'] = table.row_values(row)[self.p_col_start - 4]
                    # info['name'] = table.row_values(row)[self.p_col_start - 1]
                    # course.update(info)
            name = table.row_values(row)[self.p_col_start - 1]
            number = table.row_values(row)[self.p_col_start - 4]
            print course
                    # print table.row_values(row)[self.p_col_start-4],table.row_values(row)[self.p_col_start-1]
            values = {
                "college": self.college,
                "subject": self.subject,
                'class_': self.class_,
                "number":number,
                "name":name,
                'detail': json.dumps(course),
            }
            models.Grade(values).save()



class GridGrade(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='grade', mode='count')

        cells = ['number', 'name', 'sex', 'score', 'class_', 'course_id']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json


class GradeList(BaseManager):
    def get(self):
        params = request.args
        username = session.get('username')
        grade_info = models.Grade.query.filter_by(id=username)

        return render.grade_lists()


class GradeDelete(BaseManager):
    def post(self):
        params = request.form
        grade = models.Grade.query.filter_by(id=params.get('id')).first()
        if not grade:
            return exception2json("course is not exist")
        grade.hard_delete()
        return success2json("ok")

class GradeUpdate(BaseManager):
    def get(self):
        params = request.args
        print "----------", params.get("grade_id")
        gradeobj = models.Grade.query.filter_by(id=params.get('grade_id')).first()
        print "******",    gradeobj.id
        return render.grade_update(gradeobj=gradeobj)
    def post(self):
        params = request.form
        grade = models.Grade.query.filter_by(id=params.get('id')).first()

        id = params.get("number")
        sex = params.get("sex")
        name = params.get("name")
        score = params.get("score")

        class_ = params.get("class_")
        semester = params.get("semester")
        values ={
            "number":id,
            "sex": sex,
            "name":name,
            "score" :score,
            "class_":class_,
            "semester":semester
        }
        print "------------" ,values
        grade.update(values)
        return success2json("grade success")
class FileUPload(BaseManager):
    def get(self):
        return render.grade_upload()
class GradeDeal(BaseManager):
    def post(self):
        # file = request.files['file']
        params = request.form
        c_col_start = params.get("c_col_start")
        c_col_end = params.get("c_col_end")
        c_row_start = params.get("c_row_start")
        c_col_end = params.get("c_row_end")
        p_col_start = params.get("c_col_start")
        p_col_end = params.get("c_col_end")
        college = params.get("college")
        subject = params.get("subject")
        class_ = params.get("class_")
        print college,subject,class_
        # filename = file.filename
        # file.save(os.path.join(UPLOAD_FOLDER, filename))


        # file_url = url_for('uploaded_file', filename=filename)
        t = DealTable( 5, 12, 5, 41,college, subject, class_)
        t.deal_score()

        return  'ok'

app = Blueprint('grade_app', __name__, template_folder='templates')
app.add_url_rule('/upload', view_func=FileUPload.as_view('grade_upload'))
app.add_url_rule('/lists', view_func=GradeList.as_view('grade_lists'))
app.add_url_rule('/grid', view_func=GridGrade.as_view('grade_grid'))
app.add_url_rule('/delete', view_func=GradeDelete.as_view('grade_delete'))
app.add_url_rule('/deal', view_func=GradeDeal.as_view('grade_input'))