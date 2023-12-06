from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from firebase_admin import messaging

from django.core.cache import cache
from django.conf import settings
from app.settings import SECRET_KEY, JWT_ALGO, REDIS

def testview(request):
    dataPayLoad = {
        "type" : "newLetter",
        "taskNumber": "1",
        "content" : "편지쓰기 테스트예용"
    }
    token = "dASKYLtoTiOLgcD0MZqcyw:APA91bGr2TsOJfVNtGa53ZS_EiwTQLeHQOKPPfLi5IwcZ3ItaErYupzGFqnTzNMO1QrG3QXSLS-i2tTISvGpZeZhK4-4X8jChfIRoiwWCAuQIYr0ANb1BvEvqkk9faXeolo9crB6kz1F"
    message = messaging.Message(
        data=dataPayLoad,
        token=token
    )
    
    response = messaging.send(message=message)
    print(response)
    return response