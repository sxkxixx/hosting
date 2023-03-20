import peewee
from database import BaseModel
from user.models import User
from datetime import datetime


class Video(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(null=False, max_length=150)
    likes_amount = peewee.IntegerField(default=0)
    owner = peewee.ForeignKeyField(User, to_field='id')


class Comment(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    comment_text = peewee.CharField(max_length=500, null=False)
    owner = peewee.ForeignKeyField(User, to_field='id')
    created_at = peewee.DateTimeField(default=datetime.utcnow)
