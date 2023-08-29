from django.contrib import admin
from django.urls import path, include

from petmourning.views.letterview import *


urlpatterns = [
    path('<str:id>', handleLetter, name = 'handleLetter'),
    path('', findLetters, name = 'findLetters'),
    path('cnt', countLetters, name = 'countLetters'),
    path('community', sendLetterToCommunity, name = 'sendLetterToCommunity'),
]