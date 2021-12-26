import json
import os

import requests

REMOTE_URL = 'https://storage.googleapis.com/idss-static/movie_metadata_all.json'


def get_metadata(key='id', local_file='data/movie_metadata_all.json', remote_url=REMOTE_URL):
    '''
    Will return an object mapping from movie id to movie metadata.
    If the database file is not preset locally, it will be downloaded from a remote location.
    `key` is either `'id'` if the mapping should be movie id -> movie metadata or
    `'title'` for movie title -> move metadata
    '''
    if not os.path.exists(local_file):
        r = requests.get(remote_url, stream=True)
        if r.ok:
            print('Downloading metadata...')
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print(f'Failed to download metadata: {r.status_code}')

    with open(local_file, encoding='utf8') as f:
        data = json.load(f)
        if key == 'id':
            return data
        if key == 'title':
            return {d['netflix_title']: d for d in data.values()}
        else:
            raise ValueError(f'`{key}` is an invalid value for parameter `key`')
