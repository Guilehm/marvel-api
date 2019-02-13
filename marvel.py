import hashlib
from datetime import datetime


class Marvel:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key
        self.url = 'http://gateway.marvel.com/v1/public/'

    def get_hash(self):
        timestamp = datetime.now().timestamp()
        formatted_string = f'{timestamp}{self.private_key}{self.public_key}'
        return hashlib.md5(formatted_string.encode('utf-8')).hexdigest()
