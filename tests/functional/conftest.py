import asyncio

import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from functional.settings import test_settings


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_url, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_session: ClientSession):
    async def inner(endpoint, params):
        url = f"{test_settings.service_url}{endpoint}"
        async with aiohttp_session.get(url, params=params) as response:
            json, status = await response.json(), response.status
        return json, status
    return inner
