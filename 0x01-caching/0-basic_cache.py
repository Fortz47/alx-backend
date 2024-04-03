#!/usr/bin/env python3
"""
BasicCache Module
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """inherits from BaseCaching and is a caching system"""
    def __init__(self):
        """initialize class"""
        super().__init__()

    def put(self, key, item):
        """adds to cache"""
        if not (key is None or item is None):
            self.cache_data[key] = item

    def get(self, key):
        """retrieves from cache"""
        return self.cache_data.get(key)
