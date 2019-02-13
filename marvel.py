import hashlib
from datetime import datetime
import requests


class Marvel:
    def __init__(self, private_key, public_key, api_version='v1'):
        self.private_key = private_key
        self.public_key = public_key
        self.base_url = f'http://gateway.marvel.com/{api_version}/public/'

    def get_auth_data(self):
        timestamp = datetime.now().timestamp()
        formatted_string = f'{timestamp}{self.private_key}{self.public_key}'
        hashed_data = hashlib.md5(formatted_string.encode('utf-8')).hexdigest()
        data = dict(ts=timestamp, apikey=self.public_key, hash=hashed_data)
        return data

    def send_request(self, endpoint_path, **kwargs):
        url = f'{self.base_url}{endpoint_path}'
        params = self.get_auth_data()
        params.update(kwargs)
        return requests.get(url, params=params)
