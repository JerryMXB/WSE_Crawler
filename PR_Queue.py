import sets, heapq


class PRQueue:
    def __init__(self, limit, num_to_pr):
        self.crawled_set = sets.Set()
        self.crawl_queue = []
        self.domain_limit = {}
        self.limit = limit
        self.num_to_pr = num_to_pr
        self.count = 0

    def heapsort(self, iterable):
        length = len(iterable)
        heapq.heapify(iterable)
        return [heapq.heappop(iterable) for i in range(length)]

    def pop(self):
        return

    def push(self, my_url):
        return
