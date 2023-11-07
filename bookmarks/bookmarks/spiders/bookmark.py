import scrapy


class BookmarkSpider(scrapy.Spider):
    name = "bookmark"
    allowed_domains = ["www.test.com"]
    start_urls = ["https://www.test.com"]

    def parse(self, response):
        pass
