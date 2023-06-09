from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 60 * 3

AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = getenv('REGION_NAME')
BUCKET_NAME = getenv('BUCKET_NAME')

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')

AVATARS_DIR = getenv('AVATARS_DIR')
VIDEOS_DIR = getenv('VIDEOS_DIR')
PREVIEWS_DIR = getenv('PREVIEWS_DIR')

LINK = getenv('LINK')

SMTP_EMAIL = getenv('SMTP_EMAIL')
SMTP_PASSWORD = getenv('SMTP_PASSWORD')
SMTP_SERVER = getenv('SMTP_SERVER')

CORS_HOST = getenv('CORS_HOST')
SAME_SITE = getenv('SAME_SITE')
SECURE = bool(getenv('SECURE'))

VIDEO_CONTENT_TYPES = ['video/mp4', 'video/MPV', 'video/mpeg', 'video/ogg', 'video/webm']
IMAGE_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp']

