import jwt
from django.http import JsonResponse
from jwt.exceptions import ExpiredSignatureError
from http import HTTPStatus

from petmourning.models import User
from petmourning.exception import InvalidException, ExpiredException
from app.settings import SECRET_KEY, JWT_ALGO
from django.contrib.auth.middleware import MiddlewareMixin



# jwt로 인코딩하는 함수
def encode_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithms=JWT_ALGO).decode("utf-8")

def get_userId(request):
    userId = jwt.decode(request.headers.get("ACCESS_AUTHORIZATION", None), SECRET_KEY, algorithms=JWT_ALGO)
    userId = userId.get("userId")
    print(userId)
    return userId

def get_userName(request):
    userName = jwt.decode(request.headers.get("ACCESS_AUTHORIZATION", None), SECRET_KEY, algorithms=JWT_ALGO)
    userName = userName.get("userName", None)
    return userName

# jwt로 디코딩 하는 함수
def decode_jwt(access_token):
    return jwt.decode(
        access_token,
        SECRET_KEY,
        algorithms=[JWT_ALGO]
    )


class JsonWebTokenMiddleWare(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # if (
            #     request.path != "/api/login"
            #     and request.path != "/api/test/"
            #     and "admin" not in request.path):
            #     headers = request.headers
            #     access_token = headers.get("ACCESS_AUTHORIZATION", None)

            #     if not access_token:
            #         raise InvalidException()

            #     payload = decode_jwt(access_token)

            #     userId = payload.get("userId", None)

            #     if not userId:
            #         raise InvalidException()

            #     User.objects.get(userId=userId)

            response = self.get_response(request)

            return response

        except (InvalidException, User.DoesNotExist) as e:
            return JsonResponse(
                {"message": e.message}, status=HTTPStatus.UNAUTHORIZED, charset='utf-8'
            )
        except ExpiredSignatureError:
            return JsonResponse(
                {"message": "this token is Invalid. You should SignUp."}, status=HTTPStatus.FORBIDDEN
            )