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

from petmourning.views.loginview import kakaologin, takeFCMToken
from petmourning.views.testview import testview


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('app.otherurls.userurls')),
    path('api/home/', include('app.otherurls.homeurls')),
    path('api/letter/', include('app.otherurls.letterurls')),
    # path('/api/user', views.signUp),
    path('api/login/', kakaologin),
    path('api/fcm/token/', takeFCMToken),
    path('api/test/', testview)
]

