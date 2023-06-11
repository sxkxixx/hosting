from fastapi import UploadFile, File
from core.models import Video

VIDEO_SIGNATURES = ['66 74 79 70 4D 53 4E 56', '66 74 79 70 69 73 6F 6D', '66 74 79 70 6D 70 34 32',
                    '00 00 01 B3', '00 00 01 BA']
IMAGE_SIGNATURE = ['FF D8 FF E0', '49 46 00 01', '89 50 4E 47 0D 0A 1A 0A']


async def get_user_videos(user_id: int):
    return [{
        'id': video.id,
        'title': video.title,
        'preview_url': await video.preview_url(),
    } for video in await Video.objects.filter(Video.owner.id == user_id).all()]


def is_valid_signature(file_type: str = 'video', file: UploadFile = File(...)) -> bool:
    signature = VIDEO_SIGNATURES if file_type == 'video' else IMAGE_SIGNATURE
    file.file.seek(0)
    data = file.file.read(256)
    hex_bytes = ' '.join(['{:02X}'.format(byte) for byte in data])
    for hex_ch in signature:
        if hex_ch in hex_bytes:
            return True
    return False
