import scrapy, logging, os, shutil, string
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from nltk import word_tokenize

class ConcordiaScrapper(CrawlSpider):
    file_limit = 100 #default limit = 100
    name = "concordia"
    start_urls = [
        'https://concordia.ca',
    ]
    visited_urls = set()
    process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": int(file_limit),
        "LOG_LEVEL": "INFO"
    })
    rules = (
        Rule(LinkExtractor(deny=(r'^(?!https://www.concordia.ca).+', r'^(https://www.concordia.ca/fr).+'), ),
             callback='parse_item', follow=True),
    )
    docID = 0
    inverted_index = dict()

    def parse_item(self, response):
        if self.docID >= int(self.file_limit):
            yield self.inverted_index
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
        self.docID += 1
        self.inverted_index_builder(self.inverted_index, self.get_tf(text))

    def get_tf(self, document):
        dictionary = dict()
        for tokens in document:
            if tokens not in dictionary:
                dictionary[tokens] = 1
            else:
                dictionary[tokens] += 1
        return dictionary

    def inverted_index_builder(self, dictionary, token_tf):
        for token in token_tf.keys():
            pair = ((self.docID, token_tf[token]))
            if token not in dictionary:
                dictionary[token] = [1, [pair]]
            else:
                dictionary[token][1].append(pair)
                dictionary[token][1] = sorted(dictionary[token][1], key = lambda x: x[1], reverse=True)
                dictionary[token][0] += 1