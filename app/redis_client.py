import aioredis

redis_client = aioredis.from_url(url='redis://localhost', port=6379, db=0)

