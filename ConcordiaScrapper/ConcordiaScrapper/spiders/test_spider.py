import scrapy, logging, os, shutil
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess

class TestScrapper(CrawlSpider):
    file_limit = 100
    def __init__(self, limit=100, **kwargs):
        super().__init__(**kwargs)
        self.file_limit = limit

    name = "test"
    start_urls = [
        'http://mohanadarafe.com/',
    ]
    process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": int(file_limit),
        "LOG_LEVEL": 'INFO',
    })
    rules = (
        Rule(callback='parse_item', follow=True),
    )
    docNumber = 0

    def parse_item(self, response):
        if self.docNumber >= int(self.file_limit):
            raise CloseSpider("Limit reached.")

        url = response.url
        self.logger.info(f'Scrapping: {url}')
        with open(f'spiders/test_results/{self.docNumber}.html', 'wb') as f:
            f.write(response.body)
        self.docNumber += 1
