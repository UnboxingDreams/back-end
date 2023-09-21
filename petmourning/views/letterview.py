from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from dateutil import relativedelta
from datetime import datetime
import json
import bcrypt
import jwt

from app.settings import SECRET_KEY
from petmourning.models import User, Question, Answer, Emotion, Category, Post, MailBox
from petmourning.exception import CustomException
from petmourning.views.authorization import get_userId, get_userName


def sendLetterToCommunity(request):
    try:
        userId = get_userId(request)
        if request.method == 'POST':
            data = json.load(request.body)
            user = User.objects.get(id = userId)
            answer = Answer.objects.get(userId = userId, questionId = data.get('questionId'))
            
            if answer.postOut:
                raise CustomException("이미 커뮤니티에 존재하는 편지입니다.", status_code=400)

            post = Post.objects.create(
                userId = user,
                category = Category["LETTER"].value()
            )

            MailBox.objects.create(
                id = post,
                content = answer.content,
                contentImgUrl = answer.contentImgUrl,
                emotion = Emotion[answer.emotion.upper()].value
            )
            
            answer.postOut = True
            answer.save()

            return JsonResponse({'message' : "편지함에 편지가 등록되었습니다." }, status_code = 201)
        else:
            raise CustomException("옳바르지 않은 메소드 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '편지함에 올릴 수 없습니다.'}, status = 404) 


def countLetters(request):
    try:
        userId = get_userId(request)
        if request.method == 'GET':

            letterCnt = Answer.objects.filter(userId = userId).count()

            data = {'letterCnt' : letterCnt}

            return JsonResponse(data)
        else:
            raise CustomException("옳바르지 않은 메소드 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '요청하신 데이터에 오류가 있습니다.'}, status = 404)


def findLetters(request):
    try:
        userId = get_userId(request)
        if request.method == 'GET' and request.GET.get('date'):
            inputDate = request.GET.get('date')
            parsedDate = timezone.datetime.strptime(inputDate, "%Y-%m-%d").date()
            
            start = parsedDate.replace(day = 1)
            end = parsedDate + relativedelta.relativedelta(months=1) - timezone.timedelta(days=1)
            
            letterData = Answer.objects.filter(userId_id = userId, 
                                               createdAt__range=[start, end]).order_by('createdAt').select_related('questionId')
            data = [None] *  32

            for answer in list(letterData):
                dateData = {
                    'questionId' : answer.questionId.id,
                    'question' : answer.questionId.content,
                    'answer' : answer.content,
                    'emotion' : answer.emotion,
                    'createdAt' : answer.createdAt,
                    'postOut' : answer.postOut
                }
                data[datetime.strptime(answer.createdAt, "%Y-%m-%d %H:%M:%S").day] = dateData
                
            return JsonResponse({'letters' : data })
        else:
            raise CustomException("옳바르지 않은 메소드 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '요청하신 데이터에 오류가 있습니다.'}, status = 404) 



def handleLetter(request, id):
    try:
        userId = get_userId(request)
        if request.method == 'GET':
            question = Question.objects.get(id = id)

            data = {
                'letterId' : id,
                'content' : question.content
            }

            return JsonResponse(data)

        elif request.method == 'POST':
            user = User.objects.get(id = userId)
            question = Question.objects.get(id = id)

            data = json.loads(request.body)

            answer = Answer.objects.create(
                questionId = question,
                userId = user,
                content = data.get('content'),
                contentImgUrl = data.get('contentImgUrl'),
                postOut = data.get('postOut'),
                emotion = Emotion[data.get('emotion').upper()].value
            )

            if data.get('postOut'):
                post = Post.objects.create(
                    userId = user,
                    category = Category["LETTER"].value()
                )

                mailbox = MailBox.objects.create(
                    id = post,
                    content = data.get('content'),
                    contentImgUrl = data.get('contentImgUrl'),
                    emotion = Emotion[data.get('emotion').upper()].value
                )
            
            return JsonResponse({'postOut' : data.get('postOut')})
        
        else:
            raise CustomException("옳바르지 않은 메소드 입니다.", status_code=405)
    except CustomException as e:
        return JsonResponse({'message' : e.message}, status=e.status_code)
    except Exception:
        return JsonResponse({'message' : '요청하신 데이터에 오류가 있습니다.'}, status = 404) 
