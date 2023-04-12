import uuid
import peewee
from database import BaseModel
from user.models import User
from datetime import datetime
from video.s3_client import get_url


class Video(BaseModel):
    id = peewee.AutoField(primary_key=True)
    title = peewee.CharField(null=False, max_length=150)
    description = peewee.CharField(max_length=300)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='videos')
    cloud_name = peewee.CharField(max_length=50, unique=True)

    @property
    def url(self):
        return get_url(self.cloud_name)


class Like(BaseModel):
    id = peewee.AutoField(primary_key=True)
    user_id = peewee.ForeignKeyField(User, to_field='id')
    video_id = peewee.ForeignKeyField(Video, to_field='id')


class Comment(BaseModel):
    id = peewee.AutoField(primary_key=True, default=uuid.uuid4)
    comment_text = peewee.CharField(max_length=500, null=False)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='user_comments')
    video_id = peewee.ForeignKeyField(Video, to_field='id', backref='video_comments')
    created_at = peewee.DateTimeField(default=datetime.utcnow)
