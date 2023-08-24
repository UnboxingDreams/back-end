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


def sendNoti(token, title, content):
    noti = messaging.Notification(title=title, body=content)

    message = messaging.Message(
        notification = noti,
        token=token
    )

    response = messaging.send(message=message)

    return response