import backoff
from functional.logger import logger
from functional.settings import test_settings
from redis import Redis


@backoff.on_exception(backoff.expo, ValueError, max_time=60)
def redis_waiting():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port, socket_connect_timeout=1)
    logger.info(f"{test_settings.redis_host}")
    if not redis.ping():
        raise ValueError
    logger.info('Connected to redis "{}"'.format(test_settings.redis_host))


if __name__ == "__main__":
    redis_waiting()
