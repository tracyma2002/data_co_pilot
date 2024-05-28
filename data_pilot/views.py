from django.shortcuts import render,HttpResponse
import json
from django.db import connection
from django.http import JsonResponse
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase

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
        if username == '123' and password == '456':
            return render(request,"main.html")
        else:
            return HttpResponse("用户名或密码错误")

def search(request):
    return render(request, 'search.html')


def natural_language_to_sql_view(request):
    # 初始化大型语言模型
    llm = OpenAI(temperature=0)

    # 创建数据库连接
    db = SQLDatabase.from_uri("sqlite:///db.sqlite3")

    # 创建SQL数据库链
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    # 假设请求中包含自然语言查询
    natural_language_query = request.GET.get('query', '')

    # 使用LangChain将自然语言转换为SQL查询
    try:
        sql_query = db_chain.run(natural_language_query)

        # 执行SQL查询
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

        # 将查询结果转换为列表的字典格式
        columns = [col for col in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        # 返回JSON格式的结果
        return JsonResponse({"sql_query": sql_query, "results": results})
    except Exception as e:
        # 处理异常情况
        return JsonResponse({"error": str(e)}, status=500)
