import backoff
from elasticsearch import Elasticsearch
from functional.settings import test_settings
from functional.logger import logger


@backoff.on_exception(backoff.expo, ValueError, max_time=60)
def elastic_waiting():
    es_client = Elasticsearch(hosts=f"http://{test_settings.es_host}:{test_settings.es_port}",
                              verify_certs=False)
    logger.info(f"Checking connection to {test_settings.es_host}...")
    if not es_client.ping():
        raise ValueError


if __name__ == '__main__':
    elastic_waiting()