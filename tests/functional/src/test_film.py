import random as rd

import pytest
from functional.testdata import movies, movies_genres_counter
import uuid


@pytest.mark.parametrize(
    'film_data, expected_answer',
    [
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'film_id': rd.choice(movies)['id']},
                {'status': 200, 'length': 1}
        ),
        (
                {'uuid': str(uuid.uuid4()),},
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
                {'genre': 'Comedy', 'page_number': 1, "page_size": 50},
                {'status': 200, 'length': movies_genres_counter(genre="Comedy")}
        ),
        (
                {'genre': 'Drama', 'page_number': 1, "page_size": 50},
                {'status': 200, 'length': movies_genres_counter(genre="Drama")}
        ),
        (
                {'genre': 'Horror', 'page_number': 1, "page_size": 50},
                {'status': 200, 'length': movies_genres_counter(genre="Horror")}
        ),
        (
                {'genre': 'Something'},
                {'status': 404, 'length': 1}
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
