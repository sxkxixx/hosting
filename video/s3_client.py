import boto3



s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)