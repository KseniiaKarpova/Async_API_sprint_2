import random as rd
import pytest
from functional.testdata import genres
import uuid

@pytest.mark.parametrize(
    'expected_answer',
    [
        (
                {'status': 200, 'length': len(genres)}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_genres(make_get_request, expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint='/api/v1/genres')
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
                {'uuid': rd.choice(genres)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'uuid': str(uuid.uuid4())},
                {'status': 404, 'length': 0}
        ),
    ]
)

@pytest.mark.asyncio
async def test_get_genres_by_id(make_get_request, query,  expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=f'/api/v1/genres/{query["uuid"]}')
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
