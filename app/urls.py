"""
URL configuration for app project.

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
from django.urls import path, include

from petmourning.views.loginview import kakaologin, takeFCMToken, googlelogin, applelogin
from petmourning.views.testview import testview
from petmourning.views.homeview import *
from petmourning.views.letterview import *
from petmourning.views.userview import *
from petmourning.views.profileview import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', sendApply, name = 'sendApply'),
    path('api/home',  findHomeDisplay, name = 'findHomeDisplay'),
    path('', findProfiles, name = 'findProfiles'),
    # path('/api/user', views.signUp),
    path('api/login/kakao', kakaologin),
    path('api/login/google', googlelogin),
    path('api/login/apple', applelogin),
    path('api/fcm/token', takeFCMToken),
    path('api/test/', testview),
    path('api/letter/<int:id>', handleLetter, name = 'handleLetter'),
    path('api/letter', findLetters, name = 'findLetters'),
    path('api/letter/cnt', countLetters, name = 'countLetters'),
    path('api/letter/community', sendLetterToCommunity, name = 'sendLetterToCommunity'),
    path('api/profile', findProfiles, name="findProfiles"),
]