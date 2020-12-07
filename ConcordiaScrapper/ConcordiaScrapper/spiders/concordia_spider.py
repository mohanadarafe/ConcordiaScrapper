import scrapy, logging, os, shutil, string
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from nltk import word_tokenize

class ConcordiaScrapper(CrawlSpider):
    file_limit = 100 #default limit = 100
    def __init__(self, limit=100, **kwargs):
        super().__init__(**kwargs)
        self.file_limit = limit

    name = "concordia"
    start_urls = [
        'https://concordia.ca/',
    ]
    visited_urls = set()
    process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": int(file_limit),
        "LOG_LEVEL": "INFO"
    })
    rules = (
        Rule(LinkExtractor(deny=(r'^(?!https://www.concordia.ca).+', )),
             callback='parse_item', follow=True),
    )
    docNumber = 0

    def parse_item(self, response):
        if self.docNumber >= int(self.file_limit):
            raise CloseSpider("Limit reached.")

        url = response.url
        if url in self.visited_urls:
            self.logger.info(f'Already scrapped: {url}')
            yield
        else:
            self.visited_urls.add(url)

        self.logger.info(f'Scrapping: {url}')
        soup = BeautifulSoup(response.body, "lxml")
        text = word_tokenize(soup.get_text())
        text = [token for token in text if token not in string.punctuation]
        self.docNumber += 1

        yield {
            "url": url,
            "text": text
        }