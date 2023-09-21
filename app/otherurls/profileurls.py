from django.contrib import admin
from django.urls import path, include

from petmourning.views.profileview import *


urlpatterns = [
    path('', findProfiles, name = 'findProfiles'),
]