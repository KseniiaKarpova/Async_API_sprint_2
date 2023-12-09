import random as rd
import uuid
from http import HTTPStatus

import pytest
from functional.testdata import persons

persons_fields = ['id', 'name', 'films']
persons_detail_fields = rd.choice(persons).keys()

@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'query': rd.choice(persons)['name']},
            {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_fields}
        ),
        (
            {'query': rd.choice(persons)['name']},
            {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_fields}
        ),
        (
            {'query': 'sdasdasds'},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'fields': []}
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
    if status == HTTPStatus.OK and body:
        assert list(body[0].keys()).sort() == list(expected_answer['fields']).sort()


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
            {'uuid': rd.choice(persons)['id']},
            {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_detail_fields}
        ),
        (
            {'uuid': rd.choice(persons)['id']},
            {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_detail_fields}
        ),
        (
            {'uuid': rd.choice(persons)['id']},
            {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_detail_fields}
        ),
        (
            {'uuid': str(uuid.uuid4())},
            {'status': HTTPStatus.NOT_FOUND, 'length': 0, 'fields': []}
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
    if status == HTTPStatus.OK and body:
        assert list(body.keys()).sort() == list(expected_answer['fields']).sort()
