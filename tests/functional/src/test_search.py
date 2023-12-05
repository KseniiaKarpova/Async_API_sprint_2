import random as rd

import pytest
from functional.testdata import movies


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': movies[1]['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': movies[2]['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': movies[3]['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': movies[4]['title']},
                {'status': 200, 'length': 1}
        ),
        (
                {'query': 'Mashed potato'},
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
