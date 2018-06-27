import redis
from settings import REDIS_CONN

def redis_client():
    redis_pool = redis.ConnectionPool(host=REDIS_CONN['HOST'], port=REDIS_CONN['PORT'])
    r = redis.StrictRedis(connection_pool=redis_pool)
    return r



