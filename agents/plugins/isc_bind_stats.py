#!/usr/bin/env python3
from collections.abc import MutableMapping
import requests
import time

# https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
def flatten(dictionary, parent_key='', separator='.'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items) 

print('<<<isc_bind_stats>>>')
print('[server]')
print('current-timestamp', time.time())
resp = requests.get(url="http://localhost:8080/json/v1/server")
data = resp.json()
for key, value in flatten(data).items():
    print(key, value)
