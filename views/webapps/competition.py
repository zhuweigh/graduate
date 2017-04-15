#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/competition', encoding='utf-8',)

class CompetitionAddButton(BaseManager):
    def get(self):
        print "ooooooooooooo"
        return render.add_button()
class CompetitionAdd(BaseManager):
    def get(self):
        return  render.competition_add()
    def post(self):
        params = request.form
        values = {
            "members":params.get("members"),
            "numbers":params.get("numbers"),
            "title":params.get("title"),
            "type":params.get("type"),
            "time":params.get("time"),
        }
        print "-----------", values
        # models.Competition(values).save()
        return success2json("create com ok")
class CompetitionDelete(BaseManager):
    def get(self):
        pass

app = Blueprint('competition_app', __name__, template_folder='templates')
app.add_url_rule('/addbutton', view_func=CompetitionAddButton.as_view('competition_addbutons'))
app.add_url_rule('/add', view_func=CompetitionAdd.as_view('competition_add'))

# app.add_url_rule('/create', view_func=CourseCreate.as_view('course_create'))
# app.add_url_rule('/update', view_func=CourseUpdate.as_view('course_update'))
