import json


def get_data(path: str):
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data
