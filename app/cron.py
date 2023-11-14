from django.db.models import Max, Q, F
from django.db.models.functions import Coalesce
from petmourning.models import User, Question
from petmourning.service.FCMservice import sendNoti
from django.core.cache import cache
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger





def start():
    sched = BackgroundScheduler()
    #sched.add_job(sendTodayLetter, 'cron', second=10)
    sched.add_job(sendTodayLetter, 'cron', hour=9, minute=30)
    sched.start()


def sendTodayLetter():
    print(30000)
    usersWithMaxQuestionId = User.objects.annotate(questionId=Coalesce(Max('answer__questionId', filter=Q(answer__userId=F('pk'))), 0)).values('id', 'questionId')
    print(1)
    for user in usersWithMaxQuestionId:
        userId = user["id"]
        questionId = user['questionId']
        if not questionId:
            questionId = 1
        else:
            questionId += 1
        question = Question.objects.get(taskNumber=questionId)

        token = str(cache.get(userId))

        sendNoti(token, "편지가 배송되었습니다.", questionId , question.content)



def deleteUser():
    current_time = datetime.now()
    User.objects.filter(Q(expiration_time__isnull=True) | Q(expiration_time__lte=current_time)).delete()