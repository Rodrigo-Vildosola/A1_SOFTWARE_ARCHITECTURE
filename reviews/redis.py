import redis
from decouple import config

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.client = redis.StrictRedis(
                host=config('REDIS_HOST', default='localhost'),
                port=config('REDIS_PORT', default=6379),
                db=config('REDIS_DB', default=0),
                decode_responses=True
            )
        return cls._instance

    @property
    def connection(self):
        return self.client

redis_instance = RedisClient()

redis_client = redis_instance.connection

