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
    token = "eSLPrA6tZblqWaha-FGkZn:APA91bF4KAeQte5UDz_GxBUVC4FXUSit97BkzMypTbBXFf6s3z8egz4_D7xigiZG9-gCWQ-l2P9_gWYnhK50qR-KMyWe3diqmkyz4OJDidEFFvhD_FeFEZeGrxg5ZAXTL0b51oD8pXlp"
    message = messaging.Message(
        data=dataPayLoad,
        token=token
    )
    
    response = messaging.send(message=message)
    print(response)
    return response