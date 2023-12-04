import logging
import time
from redis import Redis
from functional.settings import test_settings

if __name__ == "__main__":

    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port, socket_connect_timeout=1)
    logging.warning(f"{test_settings.redis_host}")
    while True:
        if redis.ping():
            break
        time.sleep(10)

    logging.info('connected to redis "{}"'.format(test_settings.redis_host))
