from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import bcrypt
import jwt

from app.settings import SECRET_KEY
from .models import User, AnimalSpecies, Death
from .exception import CustomException


def completeApply(request):
    try:
        if request.method == 'PUT':
            # TODO token에서 userId를 가져와야 함
            userId = "testName"

            data = json.loads(request.body)

            user = User.objects.get(user)
            animalImg = AnimalSpecies.objects.get(
                 color = data.get('imgColor'),
                 name = data.get('imgName')
                 )
            
            user.update(
                userName = data.get('userName'),
                animalImgUrl = animalImg.speciesImgUrl,
                callBy = data.get('callBy'),
                animalSpecies = data.get('animalSpecies'),
                animalName = data.get('animalName'),
                animalDeathDate = data.get('animalDeathDate'),
                animalAge = data.get('animalAge'),
                death = Death[data.get('death').upper()].value, 
            )

            return JsonResponse({'message' : '데이터 업데이트가 완료되었습니다.'})
        else:
            raise CustomException("옳바르지 않은 접근 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status_code=e.status_code)
    except Exception:
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status_code = 404) 
    