from django.shortcuts import render,HttpResponse

def index(request):
    #data = request.GET['data']
    return HttpResponse("data-co-pilot")

def myhome(request):
    return render(request,"index.html")