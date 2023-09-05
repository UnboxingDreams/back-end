from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import base64
import bcrypt
import jwt
import requests
import datetime
import os

from app.settings import SECRET_KEY, JWT_ALGO
from ..models import User




# redirect_uri=http://13.125.35.24:8080/login/oauth2/code/kakao
class KakaoSignInView(APIView):
    permission_classes = [*]

    REDIRECT_URI =  os.getenv("REDIRECT_URI")

    def generate_token(payload, type):
        if type == "access":
            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        elif type == "refresh":
            exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
        else:
            raise Exception("Invalid tokenType")

    def kakaologin(self, request):
        # TODO 카카오에 code 전송
        
        # TODO
        try:
            access_token = request.data["access_token"]
            access_info = requests.get(
                "https://kapi.kako.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"}   
            ).json()

            # id에 대한 생각, password

            password = base64.b64decode(access_info["kakao-account"]["nickname"]).decode('ascii')
            

            if User.objects.filter(userId=id).exists():
                user = User.objects.get(userId = id)
                if user.password == password:
                    raise Exception()
            
            
            # TODO refresh_token
            # TODO access_token

            access_token = jwt.encode(pa)
            
            return JsonResponse(
                {
                    "message" : "로그인 되었습니다!",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token
                },
                status_code = 200
            )
        except Exception():
            return JsonResponse({'message' : '로그인 할 수 없습니다.'}, status_code = 404) 









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
    

    