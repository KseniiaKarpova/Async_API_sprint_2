import random as rd
import pytest
from functional.testdata import persons
import uuid

PERSONS = persons
ENDPOINT = '/api/v1/persons'

@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
            {'query' : rd.choice(PERSONS)['name']},
            {'status': 200, 'length': 1}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_persons(make_get_request, query, expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=ENDPOINT+'/search', params=query)
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
            {'uuid': rd.choice(PERSONS)['id']},
            {'status': 200, 'length': 1}
        ),
        (
            {'uuid': rd.choice(PERSONS)['id']},
            {'status': 200, 'length': 1}
        ),
        (
            {'uuid': str(uuid.uuid4())},
            {'status': 404, 'length': 0}
        ),
    ]
)

@pytest.mark.asyncio
async def test_get_person_by_id(make_get_request, query,  expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=ENDPOINT+f'/{query["uuid"]}')
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
