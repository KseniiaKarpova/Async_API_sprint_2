import random as rd
from http import HTTPStatus

import pytest
from functional.testdata import movies, persons
movies_fields = ['id', 'title', 'imdb_rating']
persons_fields = ['id', 'name', 'films']



@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': rd.choice(movies)['title']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': movies_fields}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'fields': []}
        )
    ]
)

@pytest.mark.asyncio
async def test_search_film(make_get_request, query_data, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint='/api/v1/films/search', params=query_data)
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
    if status == HTTPStatus.OK and body:
        assert list(body[0].keys()).sort() == list(expected_answer['fields']).sort()
             


@pytest.mark.parametrize(
    'query_data, expected_answer',
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
                {'query': rd.choice(persons)['name']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': persons_fields}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'fields': []}
        )
    ]
)

@pytest.mark.asyncio
async def test_search_person(make_get_request, query_data, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint='/api/v1/persons/search', params=query_data)
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
    if status == HTTPStatus.OK and body:
        assert list(body[0].keys()).sort() == list(expected_answer['fields']).sort()
