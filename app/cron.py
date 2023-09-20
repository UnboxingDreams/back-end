from django.db.models import Max, Q, F
from django.db.models.functions import Coalesce
from ..petmourning.models import User, Question
from petmourning.service.FCMservice import sendNoti
from app.settings import REDIS

def sendTodayLetter():
    usersWithMaxQuestionId = User.objects.annotate(questionId=Coalesce(Max('answer__questionId', filter=Q(answer__userId=F('pk'))), 0)).values('id', 'questionId')

    for user in usersWithMaxQuestionId:
        userId = user["id"]
        questionId = user['questionId']
        if not questionId:
            questionId = 1
        else:
            questionId += 1
        question = Question.objects.get(taskNumber=questionId)["content"]

        token = REDIS.hget("Token" + userId, "firebaseToken")
        
        sendNoti(token, "편지가 배송되었습니다.", questionId , question)

        