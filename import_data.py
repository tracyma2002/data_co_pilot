# import_data.py
from django.db import transaction  # 添加这行导入 transaction

import os
import django

# 设置Django项目的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_co_pilot.settings")

# 调用 django.setup() 来初始化 Django
django.setup()

import pandas as pd
from data_pilot.models import Student
# 假设你的Excel文件名为 '信息学院奉贤校区学生名册-2021级.xlsx'
EXCEL_FILE_PATH = 'student-information.xlsx'

from django.db.models import F, Max


def import_students():
    df = pd.read_excel(EXCEL_FILE_PATH)
    max_id = Student.objects.aggregate(max_id=Max('id'))['max_id']
    if max_id is None:
        start_id = 1
    else:
        start_id = max_id + 1
    with transaction.atomic():
        for index, row in df.iterrows():
            Student.objects.create(
                id=start_id,
                student_id=row['学号'],
                name=row['姓名'],
                class_year=row['年级'],
                class_name=row['班级'],
                gender=row['性别'],
                contact=row['联系方式'],
                dorm_building=row['宿舍楼号'],
                dorm_number=row['宿舍号'],
                status=row['类型'],
                advisor=row['班导师'],
                counselor=row['辅导员'],
                notes=row['备注']
            )
            start_id += 1
if __name__ == '__main__':
    import_students()