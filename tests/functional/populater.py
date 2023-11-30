import random
import uuid
from pathlib import Path

from elasticsearch import Elasticsearch, helpers
from faker import Faker
from functional.settings import test_settings
from functional.testdata.config import (GENRES_DATA_PATH, MOVIES_DATA_PATH,
                                        PERSONS_DATA_PATH, genres_names,
                                        roles_names)
from functional.testdata.es_mapping import genres, movies, persons

fake = Faker()
import copy
import json

BASE_DIR = Path(__file__).resolve().parent

class FakeDataCreater:
    def __init__(self, numb_data: int) -> None:
        self.num_data = numb_data
        self.film_genres = genres_names
        self.person_roles = roles_names
        persons = self.persons_generator()
        setattr(self, 'persons', persons)

        genres = self.genres_generator()
        setattr(self ,'genres', genres)

        movies = self.movies_generator()
        setattr(self, 'movies', movies)

        persons_with_movies = self.persons_with_movie_generator()
        setattr(self, 'persons', persons_with_movies)

        self.add_index(data=genres, index='genres', attribuete='genres_bulk')
        self.add_index(data=movies, index='movies', attribuete='movies_bulk')
        self.add_index(data=persons_with_movies, index='persons', attribuete='persons_bulk')

    def add_index(self, data, index, attribuete):
        objects = copy.deepcopy(data)
        bulk_query: list[dict] = [
            {'_index': index, '_id': row['id'], '_source': row}
            for row in objects]
        setattr(self, attribuete, bulk_query)
        return bulk_query

    @property
    def number(self):
        return 2 if self.num_data <= 0 else self.num_data

    @property
    def genres_random_number(self):
        return fake.random.randint(1, self.number)
    
    @property
    def writers_random_number(self):
        return fake.random.randint(1, 2 if self.number <=2 else 2)
    
    @property
    def actors_random_number(self):
        return fake.random.randint(1, 2 if self.number <=2 else self.number)

    def movie_characters(self, role: str, movie_id):
        '''
        get random persons for role
        '''
        persons = getattr(self, 'persons', self.persons_generator())
        if role == 'actor':
            characters = random.sample(persons, self.actors_random_number)
        elif role == 'writer':
            characters = random.sample(persons, self.writers_random_number)
        elif role == 'director':
            characters = random.sample(persons, 1)

        """
        save the person movie role
        """
        for person in characters:
            person_films = getattr(self, person['id'], {})
            try:
                person_films[movie_id] += [role]
            except KeyError:
                person_films[movie_id] = [role]
            setattr(self, person['id'], person_films)
        return characters, [person['name'] for person in characters]


    def genres_generator(self):
        """
        generate random genres list
        """
        return [{'id': str(uuid.uuid4()), 'name': genre_name} for genre_name in self.film_genres]
    
    def persons_generator(self):
        """
        generate random persons list without linking movies
        """
        return [{'id': str(uuid.uuid4()), 'name': fake.name()} for _ in range(self.number)]
    
    def persons_with_movie_generator(self):
        """
        extracting person movies roles
        and linking movies with persons
        """
        persons = getattr(self, 'persons', [])
        persons_with_movies = copy.deepcopy(persons)
        for person in persons_with_movies:
            person_movies = getattr(self, person['id'], {})
            for key, item in person_movies.items():
                ## create films dict based on person mappings
                person['films'] = {
                    "id": key,
                    'roles': item}
        return persons_with_movies
        
    def movies_generator(self):
        """
        generate movies list
        """
        genres = getattr(self, 'genres', self.genres_generator())
        movies = []
        for _ in range(self.number):
            movie_genre = random.sample(genres, self.genres_random_number)
            movie_id = str(uuid.uuid4())
            writers = self.movie_characters(role='writer', movie_id=movie_id)
            actors = self.movie_characters(role='actor', movie_id=movie_id)
            director = self.movie_characters(role='director', movie_id=movie_id)
            movies.append({
                'id': movie_id,
                'imdb_rating': fake.pyfloat(left_digits=1, right_digits=1, positive=True, min_value=1.0, max_value=10.0),
                'genre': movie_genre,
                'title': fake.catch_phrase(),
                'description': fake.text(),
                'director': director[0],
                'actors_names': actors[1],
                'writers_names': writers[1],
                'actors': actors[0],
                'writers': writers[0],
            })
        return movies
    

def create_index_data(objects: list[dict], state_key: str, mappings: dict, index: str):
    es = Elasticsearch(hosts=[test_settings.es_url], verify_certs=False)
    with es as client:
        if client.indices.exists(index=index):
            client.indices.delete(index=index)
        client.indices.create(index=index, body=mappings, ignore=400)
        updated, errors = helpers.bulk(client=client, actions=objects)


def save_json(path, objects):
    with open(path, 'w') as outfile:
        json.dump(objects, outfile, indent=4)


def populate():
    data_creater = FakeDataCreater(numb_data=10)
    MOVIES_MAPPING = movies
    GENRES_MAPPING = genres
    PERSONS_MAPPING = persons

    MOVIES_OBJECTS_BULK = data_creater.movies_bulk
    GENRES_OBJECTS_BULK = data_creater.genres_bulk
    PERSONS_OBJECTS_BULK = data_creater.persons_bulk

    MOVIES_OBJECTS = data_creater.movies
    GENRES_OBJECTS = data_creater.genres
    PERSONS_OBJECTS = data_creater.persons

    create_index_data(objects=MOVIES_OBJECTS_BULK, mappings=MOVIES_MAPPING, state_key='movies', index='movies')
    create_index_data(objects=GENRES_OBJECTS_BULK, mappings=GENRES_MAPPING, state_key='genres', index='genres')
    create_index_data(objects=PERSONS_OBJECTS_BULK, mappings=PERSONS_MAPPING, state_key='persons', index='persons')
    
    save_json(path=MOVIES_DATA_PATH, objects=MOVIES_OBJECTS)
    save_json(path=GENRES_DATA_PATH, objects=GENRES_OBJECTS)
    save_json(path=PERSONS_DATA_PATH, objects=PERSONS_OBJECTS)
    

if __name__ == '__main__':
    populate()
