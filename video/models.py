import uuid
import peewee
from database import BaseModel
from user.models import User
from datetime import datetime
from video.s3_client import s3, bucket_name


class Video(BaseModel):
    id = peewee.AutoField(primary_key=True)
    title = peewee.CharField(null=False, max_length=150)
    description = peewee.CharField(max_length=300)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='videos')
    cloud_name = peewee.CharField(max_length=50, unique=True)

    @property
    def url(self):
        url = s3.generate_presigned_url(
            'get_object',
            Params={"Bucket": bucket_name, "Key": self.cloud_name}, ExpiresIn=300
        )
        return url


class Like(BaseModel):
    id = peewee.AutoField(primary_key=True, default=uuid.uuid4)
    user_id = peewee.ForeignKeyField(User, to_field='id')
    video_id = peewee.ForeignKeyField(Video, to_field='id')


class Comment(BaseModel):
    id = peewee.AutoField(primary_key=True, default=uuid.uuid4)
    comment_text = peewee.CharField(max_length=500, null=False)
    owner_id = peewee.ForeignKeyField(User, to_field='id', backref='user_comments')
    video_id = peewee.ForeignKeyField(Video, to_field='id', backref='video_comments')
    created_at = peewee.DateTimeField(default=datetime.utcnow)
