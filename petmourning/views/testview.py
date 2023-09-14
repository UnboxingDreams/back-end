from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


from django.core.cache import cache
from django.conf import settings
from app.settings import SECRET_KEY, JWT_ALGO, REDIS

def testview(request):
    token = REDIS.hget("Token", "refreshToken").decode("utf-8")
    print(token)
    return HttpResponse()