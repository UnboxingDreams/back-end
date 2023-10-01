from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import json
import bcrypt
import jwt

from app.settings import SECRET_KEY, FRONT_URL
from petmourning.models import Answer, User
from petmourning.exception import CustomException
from petmourning.views.authorization import get_userId, get_userName


def findHomeDisplay(request):
    try:
        if request.method == 'GET':
            userId = get_userId(request)
            if User.objects.get(userId = userId).animalImgUrl == None:
                return redirect(FRONT_URL + "/login/SelectDog")

            animalImgUrl = User.objects.get(userId = userId).animalImgUrl

            data = {
                "animalImgUrl" : animalImgUrl
            }

            return JsonResponse(data)
        else:
            raise CustomException("옳바르지 않은 접근 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status = 404)