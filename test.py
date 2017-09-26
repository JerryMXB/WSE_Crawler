import MyUrl
import PR_Crawler
from collections import deque
import numpy as np
import urllib2

# url1 = MyUrl.MyUrl("https://www.baidu.com")
# links = ["https://www.baidu2.com"]
# url1.links = links
# url2 = MyUrl.MyUrl("https://www.baidu2.com")
# url3 = MyUrl.MyUrl("https://www.baidu3.com")
#
# urls = [url1, url2, url3]
# urls = PR_Crawler.PR_Crawler.set_page_rank(urls)
#
# for url in urls:
#     print url.url + " " + str(url.page_rank) + "\n"
# d = deque()
# d.append('hehe1')
# d.append('hehe2')
# d.append('hehe1')
# d.append('hehe3')
#
# print d

# a = np.ones(5) * 0.5
# b = np.ones(shape=(5, 5))
#
# c = a.dot(b)
# print c
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }
request = urllib2.Request("https://messenger.fb.com/wp-content/uploads/2017/04/1082-k16-david-marcus-v2.mp4", None, headers)
response = urllib2.urlopen(request)
print response.info().type