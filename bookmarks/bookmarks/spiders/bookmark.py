import scrapy
import time
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import NotSupported

# should be considering using this data - https://commoncrawl.org/

def clean_url(url):
    # remove leading and trailing double quotes
    if url[:1] == '"':
        url = url[1:]

    if url[-1:] == '"':
        url = url[:-1]

    return url


class BookmarkSpider(scrapy.Spider):
    name = "bookmark-meta"

    def read_urls_from_file(self, file_path):
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file]
        return urls

    def start_requests(self):
        urls = self.read_urls_from_file('../data/csv/bookmarks_urls.csv')
        row = 0
        for url in urls:
            row += 1
            # clean up url
            url = clean_url(url)
            yield scrapy.Request(url=url, callback=self.parse, 
                                 errback=self.errback_httpbin, 
                                 cb_kwargs=dict(row=row))

    def parse(self, response, row):
        yield {
            "url": response.url,
            "status": response.status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "row": row
        }

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.info(f"row={failure.request.cb_kwargs['row']}, {repr(failure)}")

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        status = 0
        url = None

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            url = failure.value.response.url
            self.logger.error("HttpError on %s", url)

        elif failure.check(DNSLookupError):
            # this is the original request
            url = failure.request.url
            self.logger.error("DNSLookupError on %s", url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            url = failure.request.url
            self.logger.error("TimeoutError on %s", url)
    
        elif failure.check(NotSupported):
            url = failure.request.url
            self.logger.error("NotSupported on %s", url)

        yield {
            "url": url,
            "status": status,
            "message": str(failure.value),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "row": failure.request.cb_kwargs['row']
        }

