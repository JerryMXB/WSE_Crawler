
class MyUrl:
    def __init__(self, url):
        self.url = url
        self.page_rank = 0.0
        self.links = []

    def __cmp__(self, other):
        return cmp(other.page_rank, self.page_rank)
