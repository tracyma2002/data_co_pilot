from django.shortcuts import render,HttpResponse
import json
from django.db import connection
from django.http import JsonResponse
# from langchain.llms import OpenAI
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain.utilities import SQLDatabase
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse
#from data import models
from django.db.models import Avg,Max,Min,Count,Sum,F ,Q #   引入函数
# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.db import connection
from . import api
import logging

# 引入日志记录器
logger = logging.getLogger(__name__)

def index(request):
    #data = request.GET['data']
    return HttpResponse("data-co-pilot")

def myhome(request):
    return render(request,"index.html")


def home(request):
    # 检查请求方法是否为POST
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.POST['database_account']
        password = request.POST['database_password']

        # 这里应该有一个真实的用户认证逻辑，比如检查数据库中的用户
        # 为了示例，我们假设用户名是'123'，密码是'456'
        if username == '123456' and password == '456':
            return render(request,"main.html")
        else:
            return HttpResponse("用户名或密码错误")


def register(request):
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 验证输入数据的有效性
        if not username or not password or not email:
            return JsonResponse({"error": "所有字段都是必填的"}, status=400)

        # 检查用户名是否已存在
        try:
            user = User.objects.get(username=username)
            return JsonResponse({"error": "用户名已存在"}, status=400)
        except User.DoesNotExist:
            pass

        # 创建新用户
        try:
            User.objects.create_user(username=username, email=email, password=make_password(password))
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # 注册成功后，重定向到登录页面或其他页面
        return redirect('login')  # 假设有一个名为 'login' 的登录视图函数

    # 如果是GET请求，显示注册表单
    else:
        return render(request, 'register.html')

def search(request):
    return render(request, 'search.html')


# def natural_language_to_sql_view(request):
#     # 初始化大型语言模型
#     llm = OpenAI(temperature=0)
#
#     # 创建数据库连接
#     db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
#
#     # 创建SQL数据库链
#     db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
#
#     # 假设请求中包含自然语言查询
#     natural_language_query = request.GET.get('query', '')
#
#     # 使用LangChain将自然语言转换为SQL查询
#     try:
#         sql_query = db_chain.run(natural_language_query)
#
#         # 执行SQL查询
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query)
#             rows = cursor.fetchall()
#
#         # 将查询结果转换为列表的字典格式
#         columns = [col for col in cursor.description]
#         results = []
#         for row in rows:
#             results.append(dict(zip(columns, row)))
#
#         # 返回JSON格式的结果
#         return JsonResponse({"sql_query": sql_query, "results": results})
#     except Exception as e:
#         # 处理异常情况
#         return JsonResponse({"error": str(e)}, status=500)
#

def add_query(request):
    # 您的 SQL 查询字符串
    sql_query = api.get_sql()

    try:
        # 获取数据库连接
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchall()

        # 打印结果
        for row in result:
            print(row[0])  # 假设查询结果的第一列是 price

        return HttpResponse(result)

    except Exception as e:
        # 记录错误日志
        logger.error("数据库查询出错: %s", e)
        # 返回错误信息
        return HttpResponse("您输入的查询语言有问题，请仔细检查后再查询。")
