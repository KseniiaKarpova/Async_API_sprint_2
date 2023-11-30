import random as rd

import pytest
from functional.testdata.config import MOVIES_DATA_PATH

from functional.testdata import get_data

MOVIES = get_data(path=MOVIES_DATA_PATH)

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий. 
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
