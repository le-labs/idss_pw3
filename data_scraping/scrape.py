import glob
import json
import os
from functools import cache
from pathlib import Path

import requests
import tmdbsimple as tmdb
import tqdm

# plaintext api key, wohooo
tmdb.API_KEY = 'c0581b98574e705922b594d7503de5d2'


@cache
def get_genre_map():
    r = requests.get('https://api.themoviedb.org/3/genre/movie/list',
                     params={'api_key': tmdb.API_KEY})
    data = r.json()
    return {g['id']: g['name'] for g in data['genres']}


def get_movie_data(movie_title):
    search = tmdb.Search()
    search.movie(query=movie_title)

    result = {
        'title': movie_title,
    }

    if search.total_results > 0:
        result.update(search.results[0])

        genre_map = get_genre_map()
        result['genres'] = [genre_map[g_id] for g_id in result.get('genre_ids', [])]

        for k in 'poster_path', 'backdrop_path':
            if result[k] is not None:
                result[k] = f'https://image.tmdb.org/t/p/w500{result[k]}'

    return result


def get_movie_titles():
    with open('../frontend/src/data/titles.json') as f:
        return json.load(f)


def scrape_all():
    titles = get_movie_titles()

    for movie_id, movie_title in tqdm.tqdm(titles.items(), desc='Loading movie data'):
        file = f'data/metadata/{movie_id}.json'

        if os.path.exists(file):
            continue

        details = get_movie_data(movie_title)
        with open(file, 'w', encoding='utf8') as f:
            json.dump(details, f, ensure_ascii=False)


def combine_metadata_files():
    files = glob.glob('data/metadata/*.json')

    combined = {}

    total = 0
    total_bytes = 0
    for file in tqdm.tqdm(files, desc='Combining JSON files'):
        with open(file, 'r', encoding='utf8') as f:
            data = json.load(f)
            total_bytes += f.tell()
            total += 1
            movie_id = Path(file).stem
            combined[movie_id] = data

    print(f'Total files: {total}, {total_bytes} bytes')

    with open('data/movie_metadata_all.json', 'w', encoding='utf8') as f:
        json.dump(combined, f, ensure_ascii=False, sort_keys=True)


def load_metadata():
    with open('data/movie_metadata_all.json', 'r', encoding='utf8') as f:
        return json.load(f)


if __name__ == '__main__':
    # scrape_all()
    # combine_metadata_files()

    # data = load_metadata()
    # print(data)

    pass
