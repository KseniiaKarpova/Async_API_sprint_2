from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    es_host: str = Field('test_elasticsearch', env='ES_HOST')
    es_port: str = Field('9200', env='ES_PORT')
    redis_host: str = Field('cache', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')
    redis_db: str = Field('1', env='REDIS_DB')
    service_url: str = Field('http://test_async_api:7000', env='SERVICE_URL')

    @property
    def es_url(self):
        return f"http://{self.es_host}:{self.es_port}"


test_settings = TestSettings()
