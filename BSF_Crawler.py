import urllib2, htmllib, Queue, sets, sys, fileinput
import json
import re
from bs4 import BeautifulSoup


class BSFCrawler:
    def __init__(self):
        self.hello = "The BSF Crawler starts.\n"
        self.keyword = "nyu"
        self.num = 10

    def start(self):
        print self.hello + "The keyword is: " + self.keyword + ".\nNumber of start page is: " + str(self.num) + ".\n"

        crawl_queue = Queue.Queue()
        crawled_set = sets.Set()
        start_pages = BSFCrawler.get_start_pages(self.keyword, self.num)
        for page in start_pages:
            crawl_queue.put_nowait(page)

        # The Maximum number of pages to crawl
        count = 0
        while not crawl_queue.empty() and count < 1000:
            page_to_crawl = crawl_queue.get_nowait()
            if page_to_crawl not in crawled_set:
                try:
                    links = BSFCrawler.get_links(count, page_to_crawl)
                    for link in links:
                        crawl_queue.put_nowait(link)
                    print crawl_queue.qsize()
                    # Mark this page as crawled
                    crawled_set.add(page_to_crawl)
                    count += 1
                    f = open('html_files/metadata.txt', "a")
                    f.write(str(count) + ":" + page_to_crawl + "\n")
                    f.close()
                    print count
                except urllib2.HTTPError as err:
                    print err
                    pass
                except urllib2.URLError as err:
                    print err
                    pass
                except:
                    print "Failed to get links from this page: ", sys.exc_info()[0], sys.exc_info()[1]
                    # Mark this page as crawled
                    crawled_set.add(page_to_crawl)
                    raise
            else:
                print "This page has crawled:" + page_to_crawl

    # This method is used to retrieve html page
    @staticmethod
    def retrieve_url(search_url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        request = urllib2.Request(search_url, None, headers)
        response = urllib2.urlopen(request)
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
        html = BSFCrawler.retrieve_url(search_url)

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
        print url
        links = sets.Set()
        html_page = BSFCrawler.retrieve_url(url)
        BSFCrawler.write_html_to_file(count, html_page)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            links.add(link.get('href'))
            print link.get('href')
        return links

    # This method is used to download the html pages to files
    @staticmethod
    def write_html_to_file(count, html):
        f = open('html_files/000' + str(count / 10) + '.txt', "a")
        f.write(html)
        f.close()
