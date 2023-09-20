from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import base64
import bcrypt
import jwt
import requests
import datetime
import os
import requests
from time import sleep

from app.settings import SECRET_KEY, JWT_ALGO, REDIS, REDIRECT_URI, REST_API_KEY
from ..models import User
from petmourning.views.authorization import get_userId




def takeFCMToken(request):
    if request.method == "POST":
        userId = get_userId(request)
        token = request.POST.get("firebasetoken", None)
        request.header
        REDIS.hset('Token' + userId, "firebaseToken", token)
        return JsonResponse(
            {
                "message" : "전송이 완료되었습니다.",
            },
            status_code = 201
        )


def generate_token(type, id, name):
    if type == "access":
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    elif type == "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    else:
        raise Exception("Invalid tokenType")
    payload = {
        'userId': id,
        'userName' : name,
        'exp' : exp
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGO)


def kakaologin(request):
    # try:
        sleep(2)
        code = request.GET.get("code", None)
        print(code)
        # Request Token
        headers = {
            "Content_Type" : "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type" : "authorization_code",
            "client_id" : "bf1749d6efdefd082868a6b86a9ceb56",
            "client_secret" : "b5iDy9QD7mnl5NielFrY8xe6IUeKVSE2",
            "redirect_uri" : "http://localhost:8000/api/login/",
            "code" : code
        }

        response = requests.post("https://kauth.kakao.com/oauth/token", headers=headers, data=body)
        print(response.json())
        if response.status_code == 200:
            token_info = response.json()
        else:
            JsonResponse({'message' : '카카오 코드가 유효하지 않습니다.'}, status_code = 404) 


        # Request Info
        access_token = token_info["access_token"]
        
        headers = {
            "Authorization" : f"Bearer {access_token}",
        }
        
        access_info = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers=headers
        )

        if access_info.status_code == 200:
            user_info = access_info.json()
        else:
            JsonResponse({'message' : '카카오 토큰이 유효하지 않습니다.'}, status_code = 404) 
        print(123)
        print(user_info)
        id = user_info["id"]
        nickname= user_info["kakao_account"]["profile"]["nickname"]
        print(nickname)
        print(type(nickname))
        password = base64.b64encode(nickname.encode('utf-8'))
        print(password)
        new_pass = base64.b64decode(password)
        print(new_pass)
        print(type(new_pass))
        # login And save
        if User.objects.filter(userId=id).exists():
            user = User.objects.get(userId = id)
            if user.password == password:
                raise Exception()
        else:
            user = User.objects.create(
                userId = id,
                password = password,
                userName = nickname
            )
        
        # generate token
        access_token = generate_token("access", user.userId, user.userName)
        refresh_token = generate_token("refresh", user.userId, user.userName)

        # redis에 보관
        # REDIS.hset("Token" + user.userId, "refreshToken", refresh_token)

        return JsonResponse(
            {
                "message" : "로그인 되었습니다!",
                "access_token" : access_token,
                "refresh_token" : refresh_token
            },
            status = 200
        )
    # except Exception():
        
    #     return JsonResponse({'message' : '로그인 할 수 없습니다.'}, status_code = 404) 







# # Create your views here.
# def login_check(func):
#     def wrapper(self, request, *args, **kwargs):
#         try:
#             access_token = request.headers.get('Authorization', None)
#             payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
#             user_id = User.objects.get(id=payload['id'])
#             request.user = user_id
#         except jwt.exceptions.DecodeError:
#             return JsonResponse({'message': 'INVALID TOKEN'}, status = 400)
#         except User.DoesNotExist:
#             return JsonResponse({'message': 'INVALID USER'}, status = 400)
#         return func(self, request, *args, **kwargs)
     
#     return wrapper

# def signUp(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         try:
#             if User.objects.filter(userId = data["userId"]).exists():
#                 return JsonResponse({"message" : "EXISTS_ID"}, status = 400)
#             user = User.objects.create(
#                 userId = data["userId"],
#                 password = bcrypt.hashpw(data["passward"].encode("UTF-8"))
#             ).save()

#             member = Member.objects.create(
#                 userId = user.userId,
#                 userName = None,
#                 callBy = None,
#                 animalName = None,
#                 animalImgUrl = None,
#                 animalAge = None,
#                 death = None
#             ).save()

#             return HttpResponse(status=200)
#         except KeyError:
#             return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
        

# @login_check
# def updateSignUp(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             member = Member.objects.get(userId = data["userId"])
#             member.userName = data["userName"]
#             member.callBy = data["callBy"]
#             member.animalName = data["animalName"]
#             member.animalImgUrl = data["animalImgUrl"]
#             member.animalAge = data["animalAge"]
#             member.death = data["death"]
#             member.save()
#             return HttpResponse(status=200)
#         except Member.DoesNotExist:
#             return JsonResponse({"error": "해당 userId를 가진 Member가 존재하지 않습니다."}, status=404)


# def signIn(request):
#     data = json.loads(request.body)

#     try:
#         if Member.objects.filter(userId = data["userId"]).exists():
#             member = Member.objects.get(userId = data["userId"])
#             if bcrypt.checkpw(data['password'].encode('UTF-8'), member.user.password.encode('UTF-8')):
#                 token = jwt.encode({'user' : member.user.id}, SECRET_KEY, algorithm='HS256').decode('UTF-8')
#                 return JsonResponse({"token": token}, status = 200)
#     except KeyError:
#         return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
    

    