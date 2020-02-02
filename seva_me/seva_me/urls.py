"""seva_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from sm_app.views import *
from mun_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main),
    path('ping/',ping),
    path('check/',check),
    path('create/',create),
    path('mun/',mun_main),
    path('chng_wrk/<int:code>',chng_wrk),
    path('done/<int:code>',done),
    path('find/',status)   
]

