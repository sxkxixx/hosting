from datetime import datetime
from database import BaseModel
import peewee
import uuid


class Role(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    role_name = peewee.CharField(max_length=30, null=False)


class User(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    username = peewee.CharField(unique=True, max_length=25, null=False)
    email = peewee.CharField(unique=True, max_length=100, null=False)
    hashed_password = peewee.CharField(null=False)
    registered_at = peewee.DateTimeField(default=datetime.utcnow, null=False)
    role = peewee.ForeignKeyField(Role, to_field='id', null=False)
    is_active = peewee.BooleanField(default=True, null=False)
    is_superuser = peewee.BooleanField(default=False, null=False)
