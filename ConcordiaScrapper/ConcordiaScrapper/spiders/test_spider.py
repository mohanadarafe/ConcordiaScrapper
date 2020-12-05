import scrapy, logging, os
from scrapy.linkextractors import LinkExtractor

class TestScrapper(scrapy.Spider):
    name = "test"

    def __init__(self, limit=100, **kwargs):
        assert int(limit) > 0, "Please enter a valid limit!"
        self.limit = limit
        self.extractor = LinkExtractor()
        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            'http://www.mohanadarafe.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        LIMIT = int(self.limit)
        if not os.path.isdir("spiders/test_results"):
            os.makedirs("spiders/test_results")

        linkCounter = 0
        for link in self.extractor.extract_links(response):
            if linkCounter < LIMIT:
                yield scrapy.Request(url = link.url, callback=self.parse_links)
            else:
                linkCounter += 1

    def parse_links(self, response):
        with open(f'spiders/test_results/0.html', 'wb') as f:
            f.write(response.body)