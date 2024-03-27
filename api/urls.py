"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('', views.main_spa),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('check_auth/', views.check_auth, name='check_auth'),
    path('get_appliances/', views.get_appliances_for_user, name='get_appliances'),
    path('add_appliance/', views.add_appliance, name='add_appliance'),
    path('get_energy_usage_for_user/', views.get_energy_usage_for_user, name='get_energy_usage_for_user'),
    path('send_message/', views.gptResponses, name='gpt_response'),
]
