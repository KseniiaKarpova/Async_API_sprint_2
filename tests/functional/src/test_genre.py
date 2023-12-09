import random as rd
import uuid
from http import HTTPStatus

import pytest
from functional.testdata import genres
genres_fields = ['id', 'name', 'description']
genres_detail_fields = rd.choice(genres).keys()


@pytest.mark.parametrize(
    'expected_answer',
    [
        (
                {'status': HTTPStatus.OK, 'length': len(genres), 'fields': genres_fields}
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
    if status == HTTPStatus.OK and body:
        assert list(body[0].keys()).sort() == list(expected_answer['fields']).sort()


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
                {'uuid': rd.choice(genres)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': genres_detail_fields}
        ),
        (
                {'uuid': rd.choice(genres)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': genres_detail_fields}
        ),
        (
                {'uuid': rd.choice(genres)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': genres_detail_fields}
        ),
        (
                {'uuid': str(uuid.uuid4())},
                {'status': HTTPStatus.NOT_FOUND, 'length': 0, 'fields': []}
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
    if status == HTTPStatus.OK and body:
        assert list(body.keys()).sort() == list(expected_answer['fields']).sort()
