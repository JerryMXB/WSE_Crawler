import urllib2, htmllib, sys, fileinput, heapq
import json
import re
import MyUrl
from bs4 import BeautifulSoup
import numpy as np
from collections import deque


class BFSCrawler:
    def __init__(self):
        self.hello = "The BSF Crawler starts.\n"
        self.keyword = "nyu"
        self.num = 10
        self.iterate = 0
        self.page_record = {}
        self.count = 0
        self.index = 0

    def start(self):
        print self.hello + "The keyword is: " + self.keyword + ".\nNumber of start page is: " + str(self.num) + ".\n"

        crawl_queue = deque()
        crawled_set = set()
        start_pages = self.get_start_pages(self.keyword, self.num)
        for page in start_pages:
            my_url = MyUrl.MyUrl(page, self.index, self.index)
            crawl_queue.append(my_url)
            self.page_record[page] = my_url
            self.index += 1

        # The Maximum number of pages to crawl
        while self.count < 20:
            while len(crawl_queue) > 0:
                if self.count > 20:
                    break
                page_to_crawl = crawl_queue.popleft()
                if page_to_crawl.url not in crawled_set:
                    try:
                        print str(self.count) + " Crawling page -> " + \
                              page_to_crawl.url + " index: " + str(page_to_crawl.index)
                        links = self.get_links(self.count, page_to_crawl.url)
                        print "Number of links: " + str(len(links)) + " "

                        neighbors = []
                        for link in links:
                            if link not in self.page_record:
                                self.page_record[link] = MyUrl.MyUrl(link, self.index, self.index)
                                neighbors.append(self.index)
                                self.index += 1
                            else:
                                neighbors.append(self.page_record[link].index)
                        self.page_record[page_to_crawl.url].neighbors = neighbors
                        # Mark this page as crawled
                        crawled_set.add(page_to_crawl.url)
                        self.count += 1
                    except urllib2.HTTPError as err:
                        self.count += 1
                        crawled_set.add(page_to_crawl.url)
                        print "Error code: " + str(err.code)
                        pass
                    except urllib2.URLError as err:
                        self.count += 1
                        crawled_set.add(page_to_crawl.url)
                        print err
                        pass
                    except:
                        print "Failed to get links from this page: ", sys.exc_info()[0], sys.exc_info()[1]
                        # Mark this page as crawled
                        crawled_set.add(page_to_crawl.url)
                        raise
                    finally:
                        print "\n"
                else:
                    self.count += 1
                    print "This page has crawled:" + page_to_crawl.url + "\n"

            for url in self.page_record:
                if url not in crawled_set:
                    crawl_queue.append(self.page_record[url])
            crawl_queue = deque(sorted(crawl_queue, reverse=True))

        print self.set_page_rank(self.page_record)

    # This method is used to retrieve html page
    @staticmethod
    def retrieve_url(search_url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        request = urllib2.Request(search_url, None, headers)
        response = urllib2.urlopen(request)
        print "Status code: " + str(response.getcode())
        html = response.read()
        return html

    # This method is used to get start pages by calling google RESTful custom search api
    @staticmethod
    def get_start_pages(keyword, num):
        # search keywords using google custom search api
        search_url = "https://www.googleapis.com/customsearch/v1?" \
                     "key=AIzaSyDEXoBbFC-hSlihNonu3CIxsw_1xjW92oQ&cx=010323686896096260502:ajzhk8we2de&q=" \
                     + keyword + "&num=" + str(num)
        print "Search url is: " + search_url + "\n"
        html = BFSCrawler.retrieve_url(search_url)

        # get start pages
        results = json.loads(html)
        items = results["items"]
        start_pages = []
        for item in items:
            start_pages.append(item["link"])
        print start_pages
        return start_pages

    # This method is used to parser html to get hyperlinks
    @staticmethod
    def get_links(count, url):
        # print url
        links = set()
        html_page = BFSCrawler.retrieve_url(url)
        BFSCrawler.write_html_to_file(count, html_page)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            links.add(link.get('href'))
            # print link.get('href')
        return links

    # This method is used to download the html pages to files
    @staticmethod
    def write_html_to_file(count, html):
        f = open('html_files/000' + str(count / 10) + '.txt', "a")
        f.write(html)
        f.close()

    def set_page_rank(self, page_record):
        # forming adjacency matrix
        g = np.zeros(shape=(len(page_record), len(page_record)), dtype=np.float)
        for url in page_record:
            if len(page_record[url].neighbors) != 0:
                num_links = 1.0 / len(page_record[url].neighbors)
                for neighbor in page_record[url].neighbors:
                    g[page_record[url].index, neighbor] = num_links
            else:
                # for leaks assume it has link to everyone
                num_links = 1.0 / len(page_record)
                g[page_record[url].index, :] = num_links
        print g
        page_ranks = self.page_rank(g)
        print page_ranks
        for url in page_record:
            page_record[url].page_rank = page_ranks[page_record[url].index]
        return page_record

    def page_rank(self, g, s=0.85):
        n = g.shape[0]
        pr0 = (1.0 / n) * np.ones(n)
        pr = np.ones(n)
        # Charge tax every time to handle sinks
        tax = ((1-s) / n) * np.ones(shape=(n, n))
        count = 0
        while not (pr0 == pr).all():
            print "Round" + str(count) + " "
            pr = pr0.copy()
            pr0 = pr.dot(s * g + tax)
            count += 1
        return pr