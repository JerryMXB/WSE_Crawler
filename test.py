import MyUrl
import PR_Crawler

url1 = MyUrl.MyUrl("https://www.baidu.com")
links = ["https://www.baidu2.com"]
url1.links = links
url2 = MyUrl.MyUrl("https://www.baidu2.com")
url3 = MyUrl.MyUrl("https://www.baidu3.com")

urls = [url1, url2, url3]
urls = PR_Crawler.PR_Crawler.set_page_rank(urls)

for url in urls:
    print url.url + " " + str(url.page_rank) + "\n"