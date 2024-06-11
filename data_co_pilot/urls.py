"""
URL configuration for data_co_pilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import data_pilot.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 将根 URL 指向包含登录表单的 index 视图
    path('', data_pilot.views.index, name='index'),
    #path('login/', data_pilot.views.myhome, name='login'),
    path('home/', data_pilot.views.home),
    path('home/search/',data_pilot.views.search),
    #path('api/nl2sql/', data_pilot.views.natural_language_to_sql_view, name='nl2sql'),
    path('home/search/sql/',data_pilot.views.add_query,name='add_query'),

]
