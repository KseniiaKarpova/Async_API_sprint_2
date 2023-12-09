import random as rd
import uuid
from http import HTTPStatus

import pytest
from functional.testdata import movies, movies_genres_counter
movies_fields = ['id', 'title', 'imdb_rating']
movies_detail_fields = rd.choice(movies).keys()

@pytest.mark.parametrize(
    'film_data, expected_answer',
    [
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': movies_detail_fields},
        ),
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': movies_detail_fields}
        ),
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': HTTPStatus.OK, 'length': 1, 'fields': movies_detail_fields}
        ),
        (
                {'film_id': str(uuid.uuid4())},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'fields': []}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_film(make_get_request, film_data, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=f"/api/v1/films/{film_data['film_id']}")
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
    if status == HTTPStatus.OK and body:
        assert list(body.keys()).sort() == list(expected_answer['fields']).sort()



@pytest.mark.parametrize(
    'genre, expected_answer',
    [
        (
                {'genre': 'Comedy', 'page_number': 1, "page_size": 50},
                {'status': HTTPStatus.OK, 'length': movies_genres_counter(genre="Comedy"), 'fields': movies_fields}
        ),
        (
                {'genre': 'Something'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'fields': []}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_films_by_genre(make_get_request, genre, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint="/api/v1/films", params=genre)
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
    if status == HTTPStatus.OK and body:
        assert list(body[0].keys()).sort() == list(expected_answer['fields']).sort()
