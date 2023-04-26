from datetime import datetime
import peewee
from app.utils.s3_client import get_url
from app.core.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_HOST


db = peewee.PostgresqlDatabase(POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Role(BaseModel):
    id = peewee.AutoField(primary_key=True)
    role_name = peewee.CharField(max_length=30, null=False)


class User(BaseModel):
    id = peewee.AutoField(primary_key=True)
    username = peewee.CharField(unique=True, max_length=25, null=False)
    email = peewee.CharField(unique=True, max_length=100, null=False)
    hashed_password = peewee.CharField(null=False)
    registered_at = peewee.DateTimeField(default=datetime.utcnow, null=False)
    role = peewee.ForeignKeyField(Role, to_field='id', null=False)
    is_active = peewee.BooleanField(default=True, null=False)
    is_superuser = peewee.BooleanField(default=False, null=False)


class Video(BaseModel):
    id = peewee.AutoField(primary_key=True)
    title = peewee.CharField(null=False, max_length=150)
    description = peewee.CharField(max_length=300)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='videos')
    cloud_name = peewee.CharField(max_length=50, unique=True)

    @property
    def url(self):
        return get_url(self.cloud_name)

    @property
    def video_likes_count(self):
        try:
            return Like.select().where(Like.video_id == self.id).count()
        except:
            return 0


class Like(BaseModel):
    id = peewee.AutoField(primary_key=True)
    user_id = peewee.ForeignKeyField(User, to_field='id')
    video_id = peewee.ForeignKeyField(Video, to_field='id', backref='video_likes')


class Comment(BaseModel):
    id = peewee.AutoField(primary_key=True)
    comment_text = peewee.CharField(max_length=500, null=False)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='user_comments')
    video_id = peewee.ForeignKeyField(Video, to_field='id', backref='video_comments')
    created_at = peewee.DateTimeField(default=datetime.utcnow)


class Watch(BaseModel):
    id = peewee.AutoField(primary_key=True)
    user_id = peewee.ForeignKeyField(User, to_field='id', backref='viewed_videos')
    video_id = peewee.ForeignKeyField(Video, to_field='id', backref='users_watched')
