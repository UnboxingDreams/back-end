from django.http import JsonResponse

from petmourning.models import User
from petmourning.exception import CustomException
from petmourning.views.authorization import get_userId, get_userName


def findProfiles(request):
    try:
        if request.method == 'GET':
            userId = get_userId(request)
            user = User.objects.get(userId = userId)
            if user == None:
                raise CustomException("유저 데이터가 존재하지 않습니다.", status_code=404)

            return JsonResponse(user)
        else:
            raise CustomException("옳바르지 않은 접근 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '데이터 베이스의 오류입니다.'}, status = 404)