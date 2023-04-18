from datetime import datetime
from app.db import BaseModel
import peewee


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
