from elasticsearch import Elasticsearch, helpers
from functional.settings import test_settings
from functional.testdata import es_mapping
from functional import testdata
from functional.utils.decorators import backoff


def bulk_data(objects, index):
    bulk_query: list[dict] = [
        {'_index': index, '_id': row['id'], '_source': row}
        for row in objects]
    return bulk_query


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def create_index_data(objects: list[dict], mappings: dict, index: str):
    es = Elasticsearch(hosts=[test_settings.es_url], verify_certs=False)
    with es as client:
        if client.indices.exists(index=index):
            client.indices.delete(index=index)
        client.indices.create(index=index, body=mappings, ignore=400)
        updated, errors = helpers.bulk(client=client, actions=objects, refresh='wait_for')


def populate():
    MOVIES_OBJECTS_BULK = bulk_data(objects=testdata.movies, index='movies')
    GENRES_OBJECTS_BULK = bulk_data(objects=testdata.genres, index='genres')
    PERSONS_OBJECTS_BULK = bulk_data(objects=testdata.persons, index='persons')

    create_index_data(objects=MOVIES_OBJECTS_BULK, mappings=es_mapping.movies, index='movies')
    create_index_data(objects=GENRES_OBJECTS_BULK, mappings=es_mapping.genres, index='genres')
    create_index_data(objects=PERSONS_OBJECTS_BULK, mappings=es_mapping.persons, index='persons')


if __name__ == '__main__':
    populate()
