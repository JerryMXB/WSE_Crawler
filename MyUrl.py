
class MyUrl:
    def __init__(self, url, index, page_rank=0.0):
        self.url = url
        self.page_rank = page_rank
        self.neighbors = []
        self.index = index

    def __cmp__(self, other):
        return cmp(other.page_rank, self.page_rank)
