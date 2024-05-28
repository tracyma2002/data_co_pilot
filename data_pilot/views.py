from django.shortcuts import render,HttpResponse
import json

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


