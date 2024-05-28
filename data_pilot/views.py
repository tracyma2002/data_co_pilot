from django.shortcuts import render,HttpResponse

def index(request):
    data = request.GET['data6']
    return HttpResponse("data-co-pilot")
