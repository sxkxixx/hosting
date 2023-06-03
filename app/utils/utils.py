from core.models import Video


async def get_user_videos(user_id: int):
    return [{
        'id': video.id,
        'title': video.title,
        'preview_url': await video.preview_url(),
    } for video in await Video.objects.filter(Video.owner.id == user_id).all()]
