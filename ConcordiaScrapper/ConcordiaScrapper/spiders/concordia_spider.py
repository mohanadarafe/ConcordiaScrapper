import scrapy, logging, os, shutil
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

class TestScrapper(CrawlSpider):
    PATH = "spiders/concordia_results"
    if not os.path.isdir(PATH):
        os.makedirs(PATH)
    else:
        shutil.rmtree(PATH)
        os.makedirs(PATH)

    name = "concordia"
    start_urls = ['https://www.concordia.ca/']
    rules = [Rule(callback='parse', follow=True)]

    def __init__(self, limit=100, **kwargs):
        assert int(limit) > 0, "Please enter a valid limit!"
        self.limit = limit
        self.extractor = LinkExtractor(deny=(r'^(?!https://www.concordia.ca).+', ))
        self.docNumber = 0
        super().__init__(**kwargs)

    def parse(self, response):
        LIMIT = int(self.limit)

        if(self.docNumber < LIMIT):
            links = self.extractor.extract_links(response)
            for index, link in enumerate(links):
                if(self.docNumber < LIMIT):
                    yield scrapy.Request(url = link.url, callback=self.link_to_html)
        else:
            raise CloseSpider('Limit reached.')

    def link_to_html(self, response):
        with open(f'spiders/concordia_results/{self.docNumber}.html', 'wb') as f:
            f.write(response.body)
            self.docNumber += 1
