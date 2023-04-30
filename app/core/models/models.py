import databases
import ormar
import sqlalchemy
from datetime import datetime
from app.core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from app.utils.s3_client import get_url, delete_object

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Role(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'roles'

    id: int = ormar.Integer(primary_key=True)
    role_name: str = ormar.String(max_length=30, nullable=False)


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(unique=True, max_length=25, nullable=False)
    email: str = ormar.String(unique=True, max_length=100, nullable=False)
    hashed_password: str = ormar.String(nullable=False, max_length=200)
    role: Role = ormar.ForeignKey(Role)
    is_superuser: bool = ormar.Boolean(default=False, nullable=False)


class Video(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'videos'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(nullable=False, max_length=150)
    description: str = ormar.String(nullable=True, max_length=300)
    owner_id: User = ormar.ForeignKey(User, related_name='videos')
    cloud_name: str = ormar.String(max_length=100, nullable=False, unique=True)

    @property
    def url(self):
        return get_url(self.cloud_name)

    @property
    async def likes_amount(self):
        try:
            return await Like.objects.filter(Like.video_id == self.id).count()
        except:
            return 0

    def delete_from_s3(self):
        delete_object(self.cloud_name)


class Like(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'likes'

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    video_id: Video = ormar.ForeignKey(Video, related_name='video_likes')


class Comment(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'comments'

    id: int = ormar.Integer(primary_key=True)
    comment_text: str = ormar.String(max_length=200, nullable=False)
    owner_id: User = ormar.ForeignKey(User, related_name='user_comments')
    video_id: Video = ormar.ForeignKey(Video, relates_name='video_comments')
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)


class View(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'views'

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User, relates_name='viewed_videos')
    video_id: Video = ormar.ForeignKey(Video, relates_name='user_views')
