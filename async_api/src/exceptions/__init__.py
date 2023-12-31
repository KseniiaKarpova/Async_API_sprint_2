from fastapi import HTTPException
from http import HTTPStatus

genres_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres Not Found")
genre_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre Not Found")

films_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
film_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")

person_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person Not Found")
persons_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Persons Not Found")