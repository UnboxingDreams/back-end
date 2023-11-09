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
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIzMDM2ODk0OTI1IiwidXNlck5hbWUiOiIiLCJleHAiOjE2OTg3MzE0MzR9.Zj_don3IyFfR136uuZZiDIHPFKH3NFLodidi4KDEcYc"
    message = messaging.Message(
        data=dataPayLoad,
        token=token
    )
    
    response = messaging.send(message=message)
    print(response)
    return response