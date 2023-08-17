# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse

# import json
# import bcrypt
# import jwt

# from app.settings import SECRET_KEY
# from .models import User


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
    

    