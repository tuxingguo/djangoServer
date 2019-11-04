"""djangoServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('write/', views.write_myApp),
    path('api/v1/search', views.search),
    path('api/v1/save', views.save),
    path('api/v1/getUserById', views.getUserById),
    path('api/v1/update', views.update),
    path('api/v1/delete', views.deleteById),


    path('book/queryBook', views.queryBook),
    path('book/addBook', views.addBook),
    path('book/deleteBook', views.deleteBook),
    path('book/updateBook', views.updateBook),

    path('login/account', views.account),
    path('register', views.register),
    path('register/checkUserName', views.checkUserName),
    path('user/currentUser', views.currentUser),
    path('user/getUserInfoById', views.getUserInfoById),

    path('kLine/queryNextTick1MinData', views.queryNextTick1MinData),
    path('kLine/calculateProfit', views.calculateProfit),

    path('category/queryCategoryList', views.queryCategoryList),
]
