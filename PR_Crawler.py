import urllib2, htmllib, Queue, sets, sys, fileinput, heapq
from urlparse import urlparse
import json
import re
import MyUrl
from bs4 import BeautifulSoup
import numpy as np
from scipy.sparse import csc_matrix


class PR_Crawler:
    def __init__(self):
        self.hello = "The PageRank Crawler starts.\n"
        self.keyword = "cat"
        self.num = 3

    def start(self):
        print self.hello + "The keyword is: " + self.keyword + ".\nNumber of start page is: " + str(self.num) + ".\n"

        crawled_set = sets.Set()
        start_pages = PR_Crawler.get_start_pages(self.keyword, self.num)
        crawl_queue = []
        for page in start_pages:
            url = MyUrl.MyUrl(page)
            crawl_queue.append(url)

        # The Maximum number of pages to crawl
        count = 0
        while crawl_queue and count < 1000:
            # Get the next page to crawl from queue
            page_to_crawl = crawl_queue[0].url
            if page_to_crawl not in crawled_set:
                try:
                    print "\nCrawling page " + page_to_crawl + " No:" + str(count)
                    links = PR_Crawler.get_links(count, page_to_crawl)
                    print "\nFinishing crawling pages"
                    print "\nThere are " + str(len(links)) + " page"
                    crawl_queue[0].links = links
                    for link in links:
                        url_link = MyUrl.MyUrl(link)
                        crawl_queue.append(url_link)
                    # Mark this page as crawled
                    crawled_set.add(page_to_crawl)

                    # Mark crawled page
                    f = open('html_files/metadata.txt', "a")
                    f.write(str(count) + ":" + page_to_crawl + "\n")
                    f.close()

                    # Calculate page rank and sort the queue
                    print "\nCalculating page rank"
                    PR_Crawler.set_page_rank(crawl_queue)
                    print "\nSorting the queue"
                    crawl_queue = PR_Crawler.heapsort(crawl_queue)
                    print "\nWriting metadata to file"
                    f = open('html_files/pr_metadata.txt', "a")
                    for url in crawl_queue:
                        f.write(str(count) + ":" + url.url.encode('utf-8') + " " + str(url.page_rank) + "\n")
                    f.close()

                    count += 1
                except urllib2.HTTPError as err:
                    print err
                    # Mark this page as crawled
                    crawled_set.add(page_to_crawl)
                    c = crawl_queue.pop(0)
                    count += 1
                    pass
                except urllib2.URLError as err:
                    print err
                    # Mark this page as crawled
                    crawled_set.add(page_to_crawl)
                    c = crawl_queue.pop(0)
                    count += 1
                    pass
                except:
                    print "Failed to get links from this page: ", sys.exc_info()[0], sys.exc_info()[1]
                    raise
            else:
                print "This page has crawled:" + page_to_crawl

    @staticmethod
    def heapsort(iterable):
        length = len(iterable)
        heapq.heapify(iterable)
        return [heapq.heappop(iterable) for i in range(length)]

    # This method is used to retrieve html page
    @staticmethod
    def retrieve_url(search_url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        request = urllib2.Request(search_url, None, headers)
        response = urllib2.urlopen(request, None, 3000)
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
        html = PR_Crawler.retrieve_url(search_url)

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
        links = sets.Set()
        html_page = PR_Crawler.retrieve_url(url)
        PR_Crawler.write_html_to_file(count, html_page)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            links.add(link.get('href'))
            # parsed_uri = urlparse(link.get('href'))
            # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            # print domain + "\n"
            # print link.get('href')
        return links

    # This method is used to download the html pages to files
    @staticmethod
    def write_html_to_file(count, html):
        f = open('html_files/000' + str(count / 10) + '.txt', "w")
        f.write(html)
        f.close()

    @staticmethod
    def set_page_rank(crawl_queue):
        g = np.zeros(shape=(len(crawl_queue), len(crawl_queue)))
        index = {}
        count = 0
        # Create an index for url
        for url in crawl_queue:
            index[url.url] = count
            count += 1
        for url in crawl_queue:
            for link in url.links:
                if link in index:
                    g[index[url.url], index[link]] = 1
        page_ranks = PR_Crawler.page_rank(g)
        count2 = 0
        for url in crawl_queue:
            url.page_rank = page_ranks[count2]
            count2 += 1

        return crawl_queue

    @staticmethod
    def page_rank(g, s=.85, maxerr=.01):
        n = g.shape[0]

        # transform G into markov matrix M
        M = csc_matrix(g, dtype=np.float)
        rsums = np.array(M.sum(1))[:, 0]
        ri, ci = M.nonzero()
        M.data /= rsums[ri]

        # bool array of sink states
        sink = rsums == 0

        # Compute pagerank r until we converge
        ro, r = np.zeros(n), np.ones(n)
        count = 0

        while np.sum(np.abs(r-ro)) > maxerr:
            print "Round" + str(count) + " "
            ro = r.copy()
            # calculate each pagerank at a time
            for i in xrange(0, n):
                # inlinks of state i
                Ii = np.array(M[:, i].todense())[:, 0]
                # account for sink states
                Si = sink / float(n)
                # account for teleportation to state i
                Ti = np.ones(n) / float(n)

                r[i] = ro.dot(Ii*s + Si*s + Ti*(1-s))
            count += 1
        # return normalized pagerank
        return r/sum(r)

