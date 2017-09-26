import sets, heapq
from collections import deque


class PRQueue:
    def __init__(self, num_to_pr):
        self.crawl_deque = deque()
        self.num_to_pr = num_to_pr
        self.count = 0

    def heapsort(self, iterable):
        length = len(iterable)
        heapq.heapify(iterable)
        return [heapq.heappop(iterable) for i in range(length)]

    def pop(self):
        self.crawl_deque.popleft()

    def push(self, my_url):
        for url in self.crawl_deque:
            if url.url == my_url.url:
                return
        self.crawl_deque.append(my_url)
        self.count += 1
        if self.num_to_pr > 0 and self.count == self.num_to_pr:
            self.heapsort(self.crawl_deque)
