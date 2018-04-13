# WSE_Crawler
## BFS Crawler

My BFS Crawler is a standard BFS crawler. It will call google search api to get a couple of pages to get started.
It starts at the start pages and explores the neighbor nodes first, before moving to the next level neighbours.
By exploring a node, it will first do some checking to see whether this node is valid or not, the checking including:

- Url blacklist checking, if a url ends with the extension in the blacklist (.pdf, .jpg). It will be parsed.
- MIME checking. Only Content-type equals "text/html" will be crawled.
- Robot Exclusion Protocol to avoid going into areas that are off-limits
- Site limit, only crawler 50 pages from the same site

Only after checking and find out this page is a valid url, then it will try to crawle this page. If urlopen this page returns
http code other than 200, this crawler will end and the Auditor will keep track of this failed crawl.

If the http code is 200, it will first download the page into local directory. Then parse the url inside this pages including
doing url join for the relative url. These url will be enqueued.

The crawler will stop if it has crawler 1000 pages or the queue is empty. When the crawler, it will calculate the pageRank
for the pages that has tried to crawl. And write the summary information in the Auditor to a file.
=============================================================================================================================

## Page Rank Crawler

My Page Rank Crawler starts like the BFS Crawler. It will call google search api to get a couple of pages to get started and then
get started. It will crawler these pages first and then get 100 pages following BFS strategies to get a meaning graph,
because at the beginning of the crawl the graph is more like a tree, the page rank does not make much sense to a tree.
Therefore, it will start by crawling like 100 or more. Crawling is like the BFS exploring, By exploring a node,
it will first do some checking to see whether this node is valid or not, the checking including:

- Url blacklist checking, if a url ends with the extension in the blacklist (.pdf, .jpg). It will be parsed.
- MIME checking. Only Content-type equals "text/html" will be crawled.
- Robot Exclusion Protocol to avoid going into areas that are off-limits
- Site limit, only crawler 50 pages from the same site

Only after checking and find out this page is a valid url, then it will try to crawler this page. If urlopen this page returns
http code other than 200, this crawler will end and the auditor will keep track of this failed crawl.
If the http code is 200, it will first download the page into local directory. Then parse the url inside this pages including
doing url join for the relative url. These url will be enqueued.

After performing crawling a certain percentage of the entire graph, it will re-do the page rank calculation. I assume that
10 new nodes will have more impact to a 50 nodes graph than a 1000 nodes graph. So the re calculation will happen every
time it has crawled 5% of the current graph.

There are three data structure design to calculate the page rank. MyUrl is used to keep information of a certain node,
including its url, neighbors


The crawler will stop if it has crawler 1000 pages or the queue is empty. When the crawler, it will calculate the pageRank
for the pages that has tried to crawl. And write the summary information in the Auditor to a file.
