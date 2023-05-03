import logging
# import boto3
import aioboto3
from app.core.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME

logging.basicConfig(filename='app/logs.log', level=logging.INFO)

# s3_client = boto3.client(
#     service_name='s3',
#     endpoint_url='https://storage.yandexcloud.net',
#     region_name=REGION_NAME,
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )

async_s3_session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


async def upload_video(file, file_name: str):
    uploaded = False
    async with async_s3_session.client('s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        try:
            await s3.upload_fileobj(file, BUCKET_NAME, file_name)
            logging.info(f'Upload Video: {file_name} uploaded')
            uploaded = True
        except Exception as e:
            logging.error(f'Upload Video: {e}')
    return uploaded


async def get_url(cloud_name):
    async with async_s3_session.client('s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        url = await s3.generate_presigned_url(
            'get_object',
            Params={"Bucket": BUCKET_NAME, "Key": cloud_name},
            ExpiresIn=300
        )
    return url


def delete_object(cloud_name):
    async with async_s3_session.client('s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        response = await s3.delete_object(Bucket=BUCKET_NAME, Key=cloud_name)
    return response
