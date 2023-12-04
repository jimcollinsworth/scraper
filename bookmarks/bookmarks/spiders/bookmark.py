import scrapy
import time
import random
import string
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import NotSupported
from urllib.parse import urlparse

# should be considering using this data - https://commoncrawl.org/

def clean_url(url):
    # remove leading and trailing double quotes
    if url[:1] == '"':
        url = url[1:]

    if url[-1:] == '"':
        url = url[:-1]

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    protocol = parsed_url.scheme
    url = f"{protocol}://{domain}"

    return url


class BookmarkSpider(scrapy.Spider):
    name = "bookmark-meta"

    def read_urls_from_file(self, file_path):
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file]
        return urls

    def start_requests(self):
        # create jobID for all these URLS
        job = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        urls = self.read_urls_from_file('../data/csv/bookmarks_urls.csv')
        #urls = self.read_urls_from_file('../data/csv/bookmark.csv')
        
        # whitelist private urls
        print(f"read {len(urls)} urls")
        urls = [x for x in urls if 'norc.' not in x and 'breaktech.' not in x and '192.168.' not in x and 'localhost' not in x]
        print(f"processing {len(urls)} urls")
 
        row = 0
        for url in urls:
            print(f"start:{row}-{url}")
            row += 1
            # clean up url
            url = clean_url(url)
            
            self.logger.info(f"start: {url}")

            yield scrapy.Request(url=url, callback=self.parse, 
                                 errback=self.errback_httpbin,
                                 meta={'dont_retry':True}, 
                                 cb_kwargs=dict(row=row, job=job))

    def parse(self, response, row, job):
        print(f"output:{row}-{response.url}")
        yield {
            "job": job,
            "row": row,
            "status": response.status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": response.url
        }

    def errback_httpbin(self, failure):
        # capture all request errors (but not file downloads?)
        # want to output an item record with details for every input URL, trying not to lose any urls when processing
        row = failure.request.cb_kwargs['row']
        print(f"error:{row}-{failure}")
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        #if failure.check(DNSLookupError):
        #   pass

        # errors either have a response or didn't even get that far
        if response := hasattr(failure.value,'response'):
            url = failure.value.response.url
            status = failure.value.response.status
            message = f"{failure.value} {failure.value.response}"
        else:
            url = failure.request.url
            status = 0
            message = f"{failure.value}"

        self.logger.error(f"http error: {status}-{message}-{row}{url}")    

        yield {
            "job": failure.request.cb_kwargs['job'],
            "row": failure.request.cb_kwargs['row'],
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": url
        }

