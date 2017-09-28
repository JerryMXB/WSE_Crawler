
class CrawlRecord:
    def __init__(self, url="", num=-1, page_rank=0.0, time=0, code=000, final_page_rank=0.0, size=0.0):
        self.num = num
        self.url = url
        self.page_rank = page_rank
        self.time = time
        self.code = code
        self.final_page_rank = final_page_rank
        self.size = size
