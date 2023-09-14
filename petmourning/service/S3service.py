import boto3
import datetime
from app.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_NAME

class S3ImgUploader:
    def __init__(self, file):
        self.file = file

    def letterUpload(self, userId):
        imageDate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
        url = 'letter' + '/' + userId +'/'+ imageDate
        
        s3_client.upload_fileobj(
            self.file, 
            AWS_STORAGE_NAME,
            url, 
            ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url