from django.contrib import admin
from django.urls import path, include

from petmourning import userviews


urlpatterns = [
    path('/api/user', userviews.completeApply, name = 'completeApply'),
]
