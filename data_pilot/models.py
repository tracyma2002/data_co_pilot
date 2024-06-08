from django.db import models

# Create your models here.
# models.py
from django.db import models

class students(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    age = models.IntegerField()
    gender = models.TextField(max_length=10)  # 假设性别字段为字符串，例如 'Male' 或 'Female'

    def __str__(self):
        return self.name

class student_profiles(models.Model):
    profile_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('students', on_delete=models.CASCADE, unique=True)
    address = models.TextField()
    phone = models.TextField()

    def __str__(self):
        return f"{self.students.name}'s Profile"

class teachers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # 假设教师姓名的最大长度为100
    subject = models.CharField(max_length=100)  # 假设科目名称的最大长度为100

    def __str__(self):
        return f"{self.name} - {self.subject}"

class courses(models.Model):
    course_id = models.AutoField(primary_key=True)  # 显式定义主键
    course_name = models.TextField(max_length=100)  # 假设课程名称的最大长度为100
    teacher = models.ForeignKey('teachers', on_delete=models.CASCADE)  # 外键关联到Teacher模型

    def __str__(self):
        return self.course_name

class student_courses(models.Model):
    student_id = models.ForeignKey('students', on_delete=models.CASCADE)
    course_id = models.ForeignKey('courses', on_delete=models.CASCADE)

    class Meta:
        # 确保学生和课程的组合是唯一的
        unique_together = ('student_id', 'course_id')

    def __str__(self):
        return f"{self.students.name} enrolled in {self.courses.course_name}"