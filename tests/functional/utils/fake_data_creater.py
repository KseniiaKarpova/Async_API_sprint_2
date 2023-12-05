## this file to generate fake data
import random
import uuid
from pathlib import Path
from faker import Faker
genres_names = [
    "Action", "Comedy", "Drama",
    "Horror", "Science Fiction", "Romance", 
    "Documentary", "Fantasy", "Thriller", "Mystery"]

roles_names = ['director', 'writer', 'actor']

import copy
fake = Faker()

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
        return fake.random.randint(1, len(genres_names) - 1)
    
    @property
    def writers_random_number(self):
        return fake.random.randint(1, 2 if self.number <=2 else 2)
    
    @property
    def actors_random_number(self):
        return fake.random.randint(1, 2 if self.number <=2 else 4)

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
        return {
            "objects": characters,
            "names": [person['name'] for person in characters]}


    def genres_generator(self):
        """
        generate random genres list
        """
        return [{'id': str(uuid.uuid4()), 'name': genre_name, 'description': fake.text()} for genre_name in self.film_genres]
    
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
                film = {
                        "id": key,
                        'roles': item}
                if not person.get('films'):
                    person['films'] = [film]
                    continue
                person['films'].append(film)
        return persons_with_movies
        
    def movies_generator(self):
        """
        generate movies list
        """
        genres = getattr(self, 'genres', self.genres_generator())
        movies = []
        for _ in range(self.number):
            genre_names = [genre["name"] for genre in genres]
            movie_genre = random.sample(genre_names, self.genres_random_number)
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
                'director': director['objects'],
                'actors_names': actors['names'],
                'writers_names': writers['names'],
                'actors': actors['objects'],
                'writers': writers['objects'],
            })
        return movies


def save_json(path, objects):
    import json
    with open(path, 'w') as outfile:
        json.dump(objects, outfile, indent=4)


def main():
    fake = FakeDataCreater(numb_data=20)
    save_json(path='persons.json', objects=fake.persons)
    save_json(path='movies.json', objects=fake.movies)
    save_json(path='genres.json', objects=fake.genres)


main()