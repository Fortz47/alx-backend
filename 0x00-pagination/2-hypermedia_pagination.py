#!/usr/bin/env python3
"""contains function and class for pagination operation"""
import csv
import math
from typing import Tuple, List, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return a tuple of size two containing a start index
    and an end index corresponding to the range of indexes
    to return in a list for those particular pagination parameters
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """return the appropriate page of the dataset"""
        assert isinstance(page, int)
        assert page > 0
        assert isinstance(page_size, int)
        assert page_size > 0
        self.dataset()
        start, end = index_range(page, page_size)
        end = min(end, len(self.__dataset))
        result = self.__dataset[start:end]
        if not result:
            return []
        return [x for x in self.__dataset[start:end]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """returens a dictionary containing pagination meta data"""
        result = self.get_page(page, page_size)
        totalPages = math.ceil(len(self.__dataset) / page_size)
        nextPage = page + 1
        prevPage = page - 1
        meta = {
            'page_size': len(result),
            'page': page,
            'data': result,
            'next_page': nextPage if nextPage < totalPages else None,
            'prev_page': prevPage if prevPage > 0 else None,
            'total_pages': totalPages
        }
        return meta
