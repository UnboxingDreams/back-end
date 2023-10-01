from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import json
import bcrypt
import jwt
from app.settings import SECRET_KEY, FRONT_URL
from petmourning.models import User, AnimalSpecies, Death
from petmourning.views.authorization import get_userId, get_userName
from petmourning.exception import CustomException


def sendApply(request):
    try:
        if request.method == 'PUT':
            userId = get_userId(request)

            data = json.loads(request.body)

            user = User.objects.get(userId = userId)
            
            user.update(
                userName = data.get('userName'),
                animalImgUrl = data.get('animalProperties'),
                callBy = data.get('callBy'),
                animalSpecies = data.get('animalSpecies'),
                animalName = data.get('animalName'),
                animalDeathDate = data.get('animalDeathDate'),
                animalAge = data.get('animalAge'),
                death = Death[data.get('death').upper()].value, 
            )

            return redirect(FRONT_URL + "/main")
        else:
            raise CustomException("옳바르지 않은 접근 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status = 404)
    