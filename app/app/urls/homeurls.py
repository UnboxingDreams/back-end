from django.contrib import admin
from django.urls import path, include

from petmourning.views.homeview import *


urlpatterns = [
    path('', findHomeDisplay, name = 'findHomeDisplay'),
]