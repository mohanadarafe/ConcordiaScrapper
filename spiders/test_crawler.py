import scrapy, logging, os, shutil, string, json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from nltk import word_tokenize

'''
The following scrapper will be used to test scrapy's library. Instead of creating a set
of HTML pages, I will use my portfolio website.

www.mohanadarafe.com
'''

class TestScrapper(CrawlSpider):
    file_limit = 100 # default limit = 100
    name = "test"
    start_urls = [
        'http://www.mohanadarafe.com/',
    ]
    visited_urls = set()
    rules = (
        Rule(
            LinkExtractor(),
            callback='parse_item', 
            follow=True),
    )
    docID = 0
    inverted_index = dict()

    def parse_item(self, response):
        if self.docID >= int(self.file_limit):
            if os.stat("test_result.json").st_size == 0:
                yield self.inverted_index
            raise CloseSpider("Limit reached.")

        url = response.url
        if url in self.visited_urls:
            self.logger.info(f'Already scrapped: {url}')
            yield

        self.logger.info(f'Scrapping doc #{self.docID + 1}: {url}')
        soup = BeautifulSoup(response.body, "lxml")
        text = word_tokenize(soup.get_text())
        text = [token.lower() for token in text if token not in string.punctuation]

        self.docID += 1
        self.visited_urls.add((url, len(text), self.docID))
        self.inverted_index_builder(self.inverted_index, self.get_tf(text))

    def get_tf(self, document):
        '''
        Gets the term-frequency of each document
        '''
        dictionary = dict()
        for tokens in document:
            if tokens not in dictionary:
                dictionary[tokens] = 1
            else:
                dictionary[tokens] += 1
        return dictionary

    def inverted_index_builder(self, dictionary, token_tf):
        '''
        Builds the inverted index in the following format
        term -> [df, [(tf, docID), (tf, docID), ...]]
        The postings list is sorted in terms of tf.
        '''
        for token in token_tf.keys():
            if(token in dictionary and dictionary[token][0] >= 50):
                continue

            pair = (self.docID, token_tf[token])
            if token not in dictionary:
                dictionary[token] = [1, [pair]]
            else:
                dictionary[token][1].append(pair)
                dictionary[token][1] = sorted(dictionary[token][1], key = lambda x: x[1], reverse=True)
                dictionary[token][0] += 1