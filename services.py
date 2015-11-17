import redis
import rq

import conf

redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)
rq_queue = rq.Queue(connection=redis)
