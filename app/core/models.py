import logging
import databases
import ormar
import sqlalchemy
from datetime import datetime
from core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from utils.s3_client import get_url, delete_object

logging.basicConfig(filename='app/logs.log', level=logging.INFO)
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def with_connect(function):
    async with database:
        await function()


async def create_roles():
    await Role.objects.create(role_name='User')
    await Role.objects.create(role_name='Admin')


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
    role: Role = ormar.ForeignKey(Role, ondelete='NO ACTION')
    is_superuser: bool = ormar.Boolean(default=False, nullable=False)
    avatar: str = ormar.String(max_length=50, nullable=True, unique=True)

    async def avatar_url(self):
        return await get_url(self.avatar) if self.avatar else None


class Video(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'videos'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(nullable=False, max_length=150)
    description: str = ormar.String(nullable=True, max_length=300)
    owner: User = ormar.ForeignKey(User, related_name='videos', ondelete='CASCADE')
    video_cloud_name: str = ormar.String(max_length=100, nullable=False, unique=True)
    preview_cloud_name: str = ormar.String(max_length=100, nullable=True, unique=True)

    async def video_url(self):
        return await get_url(self.video_cloud_name)

    async def preview_url(self):
        try:
            url = await get_url(self.preview_cloud_name)
        except Exception as e:
            logging.info(f'Preview Url: No Preview for {self.id}-id video')
            url = None
        return url

    async def likes_amount(self):
        try:
            likes_records = await Like.objects.filter(Like.video.id == self.id).all()
            return len(likes_records)
        except Exception as e:
            logging.info(f'Likes Amount: {e}')
            return 0

    async def delete_from_s3(self):
        await delete_object(self.video_cloud_name)
        await delete_object(self.preview_cloud_name)


class Like(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'likes'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, ondelete='CASCADE')
    video: Video = ormar.ForeignKey(Video, ondelete='CASCADE')


class Comment(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'comments'

    id: int = ormar.Integer(primary_key=True)
    comment_text: str = ormar.String(max_length=200, nullable=False)
    owner: User = ormar.ForeignKey(User, related_name='user_comments', ondelete='CASCADE')
    video: Video = ormar.ForeignKey(Video, related_name='video_comments', ondelete='CASCADE')
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)


class View(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'views'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, related_name='viewed_videos', nullable=True, ondelete="SET NULL")
    # TODO video: Переделать на ondelete="CASCADE"
    video: Video = ormar.ForeignKey(Video, related_name='user_views', nullable=True, ondelete="SET NULL")


class Claim(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'claims'

    CLAIMS_OBJECTS = ['comment', 'video', 'user']
    CLAIM_STATUSES = ['sent', 'approved', 'denied']

    id: int = ormar.Integer(primary_key=True)
    description: str = ormar.String(max_length=200, nullable=False)
    claim_type: str = ormar.String(max_length=15, choices=CLAIMS_OBJECTS)
    owner: User = ormar.ForeignKey(User, related_name='user_claims', ondelete='CASCADE')
    claim_object_id: int = ormar.Integer()
    status: str = ormar.String(max_length=15, choices=CLAIM_STATUSES, default='sent')


class Subscription(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'subscriptions'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, related_name='subscribes', ondelete='CASCADE')
    aim_user: User = ormar.ForeignKey(User, related_name='subscribers', ondelete='CASCADE')
