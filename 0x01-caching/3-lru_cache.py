#!/usr/bin/env python3
"""LRUCache Module """
from functools import wraps
from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


def trackKeys(func):
    """tracks items added to a que and ensure it does not exceed cache size
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        FLAG = args[0] not in self.cache_data  # Check if key in cache
        if len(self.trackItems) == self.MAX_ITEMS and FLAG:
            k = self.trackItems.pop()
            del self.cache_data[k]
            print(f'DISCARD: {k}')

        return func(self, *args, **kwargs)
    return wrapper


class LRUCache(BaseCaching):
    """inherits from BaseCaching and is a LRU caching system"""
    trackItems = None

    def __init__(self):
        """initialize"""
        super().__init__()
        self.trackItems = deque(maxlen=self.MAX_ITEMS)

    @trackKeys
    def put(self, key, item):
        """adds item to cache"""
        if not (key is None or item is None):
            self.cache_data[key] = item
            if key in self.trackItems:
                self.trackItems.remove(key)
            self.trackItems.appendleft(key)

    def get(self, key):
        """retrieves item from cache"""
        if key in self.trackItems:
            self.trackItems.remove(key)
            self.trackItems.appendleft(key)
        return self.cache_data.get(key)
