import asyncio

import pytest_asyncio
from aiohttp import ClientSession
from functional.settings import test_settings
from functional.utils.decorators import backoff


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_session: ClientSession):
    async def inner(endpoint, params=None):
        url = f"{test_settings.service_url}{endpoint}"
        async with aiohttp_session.get(url, params=params) as response:
            json, status = await response.json(), response.status
        return json, status
    return inner
