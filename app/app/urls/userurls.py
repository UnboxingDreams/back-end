from django.contrib import admin
from django.urls import path, include

from petmourning.views.userview import *


urlpatterns = [
    path('', sendApply, name = 'sendApply'),
]