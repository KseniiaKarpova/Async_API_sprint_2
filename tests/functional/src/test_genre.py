import random as rd
import pytest
from functional.testdata.config import GENRES_DATA_PATH
from functional.testdata import get_data
import uuid


GENRES = get_data(path=GENRES_DATA_PATH)
ENDPOINT = '/api/v1/genres'

@pytest.mark.parametrize(
    'expected_answer',
    [
        (
                {'status': 200, 'length': len(GENRES)}
        )
    ]
)

@pytest.mark.asyncio
async def get_genres(make_get_request, expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=ENDPOINT)
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
                {'uuid': rd.choice(GENRES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'uuid': rd.choice(GENRES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'uuid': str(uuid.uuid4())},
                {'status': 404, 'length': 0}
        ),
    ]
)

@pytest.mark.asyncio
async def get_genres_by_id(make_get_request, query,  expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=ENDPOINT+f'/{query["uuid"]}')
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']