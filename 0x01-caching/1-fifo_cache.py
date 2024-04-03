#!/usr/bin/env python3
"""FIFOCache Module """
from functools import wraps
BaseCaching = __import__('base_caching').BaseCaching


def trackKeys(func):
    """tracks items added to a dictionary from most recent to least recent
    """
    FI = 1  # First In

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        FLAG = args[0] not in self.cache_data  # Check if key in cache
        if len(self.trackItems) == self.MAX_ITEMS and FLAG:
            k = self.trackItems.get(FI)
            del self.cache_data[k]
            print(f'DISCARD: {self.trackItems[FI]}')
            del self.trackItems[FI]
            temp = {}
            for k, v in self.trackItems.items():
                temp[k - 1] = v
            self.trackItems = temp

        return func(self, *args, **kwargs)
    return wrapper


class FIFOCache(BaseCaching):
    """inherits from BaseCaching and is a caching system"""
    count = 0

    def __init__(self):
        """initialize"""
        super().__init__()
        self.trackItems = {}

    @trackKeys
    def put(self, key, item):
        """adds item to cache"""
        if self.count > self.MAX_ITEMS:
            self.count = self.MAX_ITEMS
        elif key in self.cache_data:
            pass
        else:
            self.count += 1
        if not (key is None or item is None):
            self.cache_data[key] = item
            if key not in self.trackItems.values():
                self.trackItems[self.count] = key

    def get(self, key):
        """retrieves item from cache"""
        return self.cache_data.get(key)
