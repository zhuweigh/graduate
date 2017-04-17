from xlrd import open_workbook
files = '/root/desigine/studentinfomanager/application/static/js/grade.xls'
from collections import OrderedDict
data = open_workbook(files)
print data
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
print  nrows
print  ncols
# print table.row_values(0)
# print table.col_values(1)

# row[0] [1]
course_number = table.row_values(0)
course_name = table.row_values(1)
name=''
number =''
# for row in range(4,nrows):
#     number += table.row_values(row)[1]+','
#     name += table.row_values(row)[4] +','
# print  number,  name
# course = {"score":None, "type":None,"number":None}
# people = {
#     "name":{},
#     "number":{}
# }
course = {}
info = {}

class DealTable(object):
    def __init__(self, c_col_start=None, c_col_end=None, c_row_start=None, c_row_end=None,
                 p_col_start=None, p_col_end=None, p_row_start=None, p_row_end=None):
        self.c_col_start = c_col_start
        self.c_col_end = c_col_end
        self.c_row_start = c_row_start
        self.c_row_end = c_row_end
        self.p_col_start = p_col_start
        self.p_col_end = p_col_end
        self.p_row_start = p_row_start
        self.p_row_end = p_row_end
        count = 0
    def deal_score(self):
        # print course
        count = 0
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
                    info['number'] = table.row_values(row)[self.p_col_start-4]
                    info['name'] = table.row_values(row)[self.p_col_start-1]
                    course.update(info)
                    count = count + 1
                    # print table.row_values(row)[self.p_col_start-4],table.row_values(row)[self.p_col_start-1]
            print course


t = DealTable(5, 12, 1, 4, 5, 12, 5, 18)
t.deal_score()
values = {
    "college":"tonxin",
    "subject":"diani",
    "class_":"diani131",
    "number":"2013131018",
    "name":"zhuwei",
    "semester":"2013-2014",
    "detail":{"course_a":{"score":2,"grade":99,"type":"bixiu", "number":2342},
              "course_b":{"score":3,"grade":88, "type":"fuxiu","number":23534},
             }
}
