import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

TEST_DATA_ROOT = os.path.join(BASE_DIR)
MOVIES_DATA_PATH = f'{TEST_DATA_ROOT}/movies.json'
PERSONS_DATA_PATH = f'{TEST_DATA_ROOT}/persons.json'
GENRES_DATA_PATH = f'{TEST_DATA_ROOT}/genres.json'

MOVIES_DATA_PATH_BULK = f'{TEST_DATA_ROOT}/movies_bulk.json'
PERSONS_DATA_PATH_BULK = f'{TEST_DATA_ROOT}/persons_bulk.json'
GENRES_DATA_PATH_BULK = f'{TEST_DATA_ROOT}/genres_bulk.json'

genres_names = [
    "Action", "Comedy", "Drama",
    "Horror", "Science Fiction", "Romance", 
    "Documentary", "Fantasy", "Thriller", "Mystery"]

roles_names = ['director', 'writer', 'actor']
