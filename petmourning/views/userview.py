from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.db import transaction

import json
import bcrypt
import jwt
from app.settings import SECRET_KEY, FRONT_URL
from petmourning.models import User, AnimalSpecies, Death
from petmourning.views.authorization import get_userId, get_userName
from petmourning.exception import CustomException


@transaction.atomic
def sendApply(request):
    try:
        if request.method == 'PUT':
            userId = get_userId(request)
            print("userId")

            data = json.loads(request.body)
            print("data")

            user = User.objects.get(userId = userId)
            user.userName = data.get('userName')
            user.animalImgUrl = data.get('animalProperties')
            user.callBy = data.get('callBy')
            user.animalSpecies = data.get('animalSpecies')
            user.animalName = data.get('animalName')
            user.animalDeathDate = datetime.fromisoformat(str(data.get('animalDeathDate'))).date()
            user.animalAge = data.get('animalAge')
            user.death = data.get('death')
            user.save()
            
            user = User.objects.get(userId = userId)
            print(user.death)

            return JsonResponse({'message' : '정보가 등록되었습니다.'}, status = 201)

        else:
            raise CustomException("옳바르지 않은 접근 입니다.")
    except CustomException as e:
        print(e)
        return JsonResponse({'message' : e.message}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status = 405)
    