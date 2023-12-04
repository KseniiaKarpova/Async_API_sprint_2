import random as rd

import pytest
from functional.testdata.config import MOVIES_DATA_PATH, GENRES_DATA_PATH

from functional.testdata import get_data
import uuid

MOVIES = get_data(path=MOVIES_DATA_PATH)
GENRES = get_data(path=GENRES_DATA_PATH)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': rd.choice(MOVIES)['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': rd.choice(MOVIES)['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': rd.choice(MOVIES)['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': rd.choice(MOVIES)['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': 'Mashed potato', 'page_number': 1, 'page_size': 1},
                {'status': 404, 'length': 1}
        )
    ]
)

@pytest.mark.asyncio
async def test_search(make_get_request, query_data, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint='/api/v1/films/search', params=query_data)
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']


@pytest.mark.parametrize(
    'film_data, expected_answer',
    [
        (
                {'film_id': rd.choice(MOVIES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(MOVIES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(MOVIES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(MOVIES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': str(uuid.uuid4()),},
                {'status': 404, 'length': 1}
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



@pytest.mark.parametrize(
    'genre, expected_answer',
    [
        (
                {'genre': rd.choice(GENRES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'genre': rd.choice(GENRES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'genre': rd.choice(GENRES)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'genre': str(uuid.uuid4())},
                {'status': 404, 'length': 1}
        )
    ]
)

@pytest.mark.asyncio
async def test_get_films_by_genre(make_get_request, genre, expected_answer):
    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(endpoint=f"/api/v1/films", params=genre)
    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length'] or len(body) > expected_answer['length']
