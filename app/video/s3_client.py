import boto3
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def upload_file(file):
    s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)


def get_url(file_name):
    # url = s3.get_object(Bucket=BUCKET_NAME, Key='video.MP4')
    # print(url)
    url = s3.generate_presigned_url(
        'get_object',
        Params={"Bucket": BUCKET_NAME, "Key": file_name}, ExpiresIn=300
    )
    return url
