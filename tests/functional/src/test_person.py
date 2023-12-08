import random as rd
import pytest
from functional.testdata import persons
import uuid
from http import HTTPStatus

PERSONS = persons

@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'query' : rd.choice(PERSONS)['name']},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'query' : rd.choice(PERSONS)['name']},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'query' : 'sdasdasds'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_persons(make_get_request, params, expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint='/api/v1/persons/search', params=params)
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
            {'uuid': rd.choice(PERSONS)['id']},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'uuid': rd.choice(PERSONS)['id']},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'uuid': rd.choice(PERSONS)['id']},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'uuid': str(uuid.uuid4())},
            {'status': HTTPStatus.NOT_FOUND, 'length': 0}
        ),
    ]
)

@pytest.mark.asyncio
async def test_get_person_by_id(make_get_request, query,  expected_answer):
    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=f'/api/v1/persons/{query["uuid"]}')
    # 2. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
