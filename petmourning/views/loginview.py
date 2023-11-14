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
import cryptography.hazmat.primitives.serialization as serialization
from cryptography.hazmat.primitives import serialization as primitives_serialization
import OpenSSL.crypto as crypto

from app.settings import SECRET_KEY, JWT_ALGO, REDIS, REDIRECT_URI, REST_SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, APPLE_CLIENT_ID, APPLE_ISS, APPLE_KEY_ID
from ..models import User
from petmourning.views.authorization import get_userId
from django.core.cache import cache
from oauthlib.oauth2 import WebApplicationClient



def takeFCMToken(request):
    if request.method == "POST":
        userId = get_userId(request)
        token = request.POST.get("firebasetoken", None)
        cache.set("Token" + userId, token)
        return JsonResponse(
            {
                "message" : "전송이 완료되었습니다.",
            },
            status = 201
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

def create_client_secret():
    
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(seconds=600) 

    payload = {
        "iss" : APPLE_ISS,
        "iat": current_time,
        "exp": expiration_time,
        "aud": "https://appleid.apple.com",
        "sub": "com.unboxing.pemourning"
    }

    client_secret = jwt.encode(payload, get_private_key(), algorithm="ES256", headers={
        "kid": APPLE_KEY_ID,
        "alg" : "ES256",
        "typ" : "JWT"})
    
    return client_secret

def get_private_key():
    # .p8 파일 경로
    p8_file_path = "petmourning/AuthKey.p8"

    # .p8 파일을 PEM 형식의 문자열로 읽음
    with open(p8_file_path, 'rb') as p8_file:
        p8_data = p8_file.read()

    # PEM 형식의 개인 키를 로드
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, p8_data)

    # cryptography 라이브러리의 개인 키 형식으로 변환
    private_key_bytes = private_key.to_cryptography_key().private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    return private_key_bytes


def get_user_info(access_token):
    _, encoded_payload, _ = access_token.split(".")
    payload_bytes = base64.urlsafe_b64decode(encoded_payload + "=" * (4 - len(encoded_payload) % 4))
    payload = payload_bytes.decode("utf-8")
    json_payload = json.loads(payload)
    sub = json_payload.get("sub")
    return sub

def applelogin(request):
    try:
        code = request.GET.get("code", None)
        
        headers = {
            "Content_Type" : "application/x-www-form-urlencoded"
        }

        body = "?client_id"+APPLE_CLIENT_ID+"&client_secret="+create_client_secret+"?code="+code+"?grant_type=authorization_code"

        response = request.post("https://appleid.apple.com/auth/token" + body, headers=headers)
        print(response.json())


        if response.status_code == 200:
            token_info = response.json()
        else:
            return JsonResponse({'message' : '애플 코드가 유효하지 않습니다.'}, status = 400) 
        
        access_token = token_info["access_token"]
        apple_id = get_user_info(access_token)
        password = base64.b64encode(apple_id.encode('utf-8'))

        if User.objects.filter(userId=apple_id).exists():
            user = User.objects.get(userId = apple_id)
            user.expirationTime = None
            user.save()
        else:
            user = User.objects.create(
                userId = id,
                password = password,
                userName = "에플유저",
                expirationTime = None
            )
        
        access_token = generate_token("access", user.userId, user.userName)
        refresh_token = generate_token("refresh", user.userId, user.userName)
            
        return JsonResponse(
                {
                    "message" : "로그인 되었습니다!",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token
                },
                status = 200
            )
    except Exception():
        return JsonResponse({'message' : '로그인 할 수 없습니다.'}, status = 404) 

def googlelogin(request):
    try:
        sleep(1)
        code = request.GET.get("code", None)
        headers = {
            "Content_Type" : "application/x-www-form-urlencoded"
        }


        body = "?grant_type=authorization_code&client_id=" + GOOGLE_CLIENT_ID + "&client_secret="+ GOOGLE_CLIENT_SECRET + "&redirect_uri="+REDIRECT_URI+"google&code=" + code

        print(body)
        response = requests.post("https://oauth2.googleapis.com/token" + body, headers=headers)
        print(response.json())

        if response.status_code == 200:
            token_info = response.json()
        else:

            return JsonResponse({'message' : '구글 코드가 유효하지 않습니다.'}, status = 400) 

        
        access_token = token_info["access_token"]

        access_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+access_token)


        print(response.json())
        if access_info.status_code == 200:
            user_info = access_info.json()
        else:

            return JsonResponse({'message' : '구글 토큰이 유효하지 않습니다.'}, status = 404) 

        
        id = user_info["id"]
        nickname= user_info["email"]
        
        password = base64.b64encode(nickname.encode('utf-8'))
        
        if User.objects.filter(userId=id).exists():
            user = User.objects.get(userId = id)
            user.expirationTime = None
            user.save()
        else:
            user = User.objects.create(
                userId = id,
                password = password,
                userName = nickname,
                expirationTime = None
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
    except Exception():
        
        return JsonResponse({'message' : '로그인 할 수 없습니다.'}, status = 404) 




def kakaologin(request):
    try:
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
            "client_secret" : REST_SECRET_KEY,
            "redirect_uri" : REDIRECT_URI + "kakao",
            "code" : code
        }

        response = requests.post("https://kauth.kakao.com/oauth/token", headers=headers, data=body)
        
        print(response.json())
        if response.status_code == 200:
            token_info = response.json()
        else:
            return JsonResponse({'message' : '카카오 코드가 유효하지 않습니다.'}, status = 400) 

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
            return JsonResponse({'message' : '카카오 토큰이 유효하지 않습니다.'}, status = 404) 
        
        id = user_info["id"]
        nickname= user_info["kakao_account"]["profile"]["nickname"]
        
        password = base64.b64encode(nickname.encode('utf-8'))
        
        new_pass = base64.b64decode(password)
        if User.objects.filter(userId=id).exists():
            user = User.objects.get(userId = id)
            user.expirationTime = None
            user.save()
        else:
            user = User.objects.create(
                userId = id,
                password = password,
                userName = nickname,
                expirationTime = None
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
    except Exception():
        return JsonResponse({'message' : '로그인 할 수 없습니다.'}, status = 404) 





    