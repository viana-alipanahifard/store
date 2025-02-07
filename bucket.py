import boto3
import logging
from botocore.exceptions import ClientError
from django.conf import settings

class Bucket:
    """CDN bucket manager

    init method creates connection
    """
    def __init__(self): 
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result.get('KeyCount'): 
            return result['Contents']
        else:
            return None

bucket = Bucket()


