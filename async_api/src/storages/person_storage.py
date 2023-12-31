from elasticsearch import AsyncElasticsearch, NotFoundError
from uuid import UUID
from storages.base_storage import BaseStorage
from db.elastic import get_elastic
from abc import abstractmethod


class PersonBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int) -> list | None:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: UUID) -> dict | None:
        pass

    @abstractmethod
    async def search_data(self, query, page_number: int, page_size: int) -> list | None:
        pass

    @abstractmethod
    async def get_person_films(self, id: UUID) -> list | None:
        pass


class PersonElasticStorage(PersonBaseStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = get_elastic()

    async def get_data_by_id(self, id: UUID) -> dict | None:
        try:
            doc = await self.elastic.get(index="persons", id=id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def search_data(self, query, page_number: int, page_size: int) -> list | None:
        search_query = {"query_string": {"default_field": "name", "query": query}}
        docs = await self.elastic.search(
            index="persons",
            body={
                "_source": ["id", "name", "films"],
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_person_films(self, id: UUID) -> list | None:
        try:
            filter_query = ({
                "bool": {
                    "should": [{
                        "nested": {
                            "path": "actors",
                            "query": {"bool": {"must": {"match": {"actors.id": id}}}},
                        }},
                        {"nested": {
                            "path": "writers",
                            "query": {"bool": {"must": {"match": {"writers.id": id}}}},
                        }}
                    ]
                }
            })
            docs = await self.elastic.search(
                index="movies",
                body={
                    "_source": ["id", "title", "imdb_rating", 'actors', 'writers'],
                    "query": filter_query,
                },
                params={"filter_path": "hits.hits._source"},
            )
            if not docs:
                return None
            return [film["_source"] for film in docs["hits"]["hits"]]
        except NotFoundError:
            return None

    async def get_data_list(self, page_number: int, page_size: int) -> list | None:
        docs = await self.elastic.search(
            index="persons",
            body={
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": {"match_all": {}},
            },
        )
        if not docs:
            return None
        return [person["_source"] for person in docs["hits"]["hits"]]
