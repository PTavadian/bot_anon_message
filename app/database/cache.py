import redis
from config import IS_DOCKER

host = 'redis' if IS_DOCKER else 'localhost'
redis_client = redis.Redis(host=host, port=6379, db=0) 

