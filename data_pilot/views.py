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
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
# 引入日志记录器
logger = logging.getLogger(__name__)

def index(request):
    # 确保 index 视图渲染 index.html
    return render(request, 'index.html')
# def myhome(request):
#     return render(request,"index.html")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('database_account')
        password = request.POST.get('database_password')

        # 验证输入数据的有效性
        if not username or not password:
            return HttpResponse("用户名和密码不能为空", status=400)

        # 检查用户名是否已存在
        try:
            User.objects.get(username=username)
            return HttpResponse("用户名已存在", status=400)
        except User.DoesNotExist:
            pass

        # 创建新用户，make_password自动加密密码
        user = User.objects.create_user(username=username, password=make_password(password))
        user.save()

        # 注册成功后，重定向到首页
        return redirect('index')
    else:
        # 显示注册表单
        return render(request, 'register.html')

# 登录视图函数
def home(request):
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.POST['database_account']
        password = request.POST['database_password']

        # 使用Django的authenticate函数进行用户认证
        user = authenticate(username=username, password=password)

        # 如果用户认证成功
        if user is not None:
            # 使用login函数登录用户
            login(request, user)
            # 假设登录成功后重定向到search页面
            return redirect('search')
        else:
            # 如果认证失败，返回错误信息
            return HttpResponse("用户名或密码错误", status=401)

    # 如果不是POST请求，显示登录表单
    else:
        # 这里可以添加代码来渲染并返回登录表单
        return render(request, 'index.html')


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

    sql_query = api.get_sql(request)

    try:
        # 获取数据库连接
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchall()

        request.session['query_result'] = result



        # 打印结果
        # for row in result:
        #     print(row[0])  # 假设查询结果的第一列是 price
        context = {'result': result}
        return render(request, 'search.html', context)

    except Exception as e:
        # 记录错误日志
        logger.error("数据库查询出错: %s", e)
        # 返回错误信息
        return HttpResponse("您输入的查询语言有问题，请仔细检查后再查询。")


def get_query_results(request):
    # 假设这是从数据库查询得到的原始结果
    # 这里我们使用 add_query 函数执行查询后的结果作为示例

    # 由于我们没有实际的数据库查询，我们将使用模拟数据
    mock_query_results = request.session.get('query_result', [])

    # 初始化柱状图和饼图的数据结构
    bar_categories = []
    bar_values = []
    pie_series_data = []

    # 将查询结果转换为 ECharts 所需的数据格式
    for course_name, student_count in mock_query_results:
        bar_categories.append(course_name)  # 柱状图的类别（课程名称）
        bar_values.append(student_count)  # 柱状图的值（选课学生数量）

        # 对于饼图，我们创建一个包含名称和值的对象
        pie_series_data.append({
            'name': course_name,
            'value': student_count
        })

    # 准备返回的数据结构
    echarts_data = {
        'barChartData': {
            'categories': bar_categories,  # 柱状图的类别数据
            'values': bar_values,  # 柱状图的值数据
        },
        'pieChartData': pie_series_data  # 饼图的数据
    }


    # 返回 JSON 响应
    return JsonResponse(echarts_data)

