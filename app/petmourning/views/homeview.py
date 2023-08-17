from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import bcrypt
import jwt

from app.settings import SECRET_KEY
from ..models import Answer, User
from ..exception import CustomException


def getHomeDisplay(request):
    try:
        if request.method == 'GET':
            # TODO token에서 userId를 가져와야 함
            userId = "testName"

            letterCnt = Answer.objects.filter(userId = userId).count()
            animalImgUrl = User.objects.get(userId = userId).animalImgUrl

            data = {
                "letterCnt" : letterCnt,
                "animalImgUrl" : animalImgUrl
            }

            return JsonResponse(data)
        else:
            raise CustomException("옳바르지 않은 접근 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status_code=e.status_code)
    except Exception:
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status_code = 404)