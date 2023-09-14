from firebase_admin import messaging
from app.settings import FIREBASE_APP


def sendData(token, letterId, content):
    dataPayLoad = {
        "letterId": letterId,
        "content" : content
    }

    message = messaging.Message(
        data=dataPayLoad,
        token=token
    )
    
    response = messaging.send(message=message)

    return response


def sendNoti(token, title, questionId, question):
    noti = messaging.Notification(title=title, body="새로운 편지를 확인해보세요!")

    message = messaging.Message(
        notification = noti,
        data= {
            "type" : "newLetter",
            "qeustionId" : questionId,
            "question" : question
        },
        token=token
    )

    response = messaging.send(message=message)

    return response