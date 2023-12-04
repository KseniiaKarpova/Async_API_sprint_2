from functools import lru_cache
from uuid import UUID
from db.elastic import get_elastic
from db.redis import get_redis
from redis.asyncio import Redis
from services.cache import RedisCache
from fastapi import Depends
from services.base_service import BaseService
from storages.film_storage import FilmElasticStorage
from elasticsearch import AsyncElasticsearch


class FilmService(BaseService):
    def __init__(self, cache: RedisCache, storage: FilmElasticStorage):
        self.cache = cache
        self.storage = storage

    async def search_data(self, query, page_number: int, page_size: int):
        data = await self.storage.search_data(query, page_number=page_number, page_size=page_size)
        return data

    async def get_data_by_id(self, url: str, id: UUID) -> dict:
        data = await self.cache.get_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_to_cache(url, data)
        return data

    async def get_data_list(
        self, sort: str, genre: UUID, page_number: int, page_size: int
    ) -> list[dict]:
        data = await self.storage.get_data_list(
            sort=sort, genre=genre, page_number=page_number, page_size=page_size
        )
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    redis = RedisCache(redis)
    elastic = FilmElasticStorage(elastic)
    return FilmService(redis, elastic)
