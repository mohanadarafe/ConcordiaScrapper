import scrapy, logging, os, shutil
from scrapy.linkextractors import LinkExtractor

class TestScrapper(scrapy.Spider):
    name = "test"

    def __init__(self, limit=100, **kwargs):
        assert int(limit) > 0, "Please enter a valid limit!"
        self.limit = limit
        self.extractor = LinkExtractor()
        self.linkNumber = 0
        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            'http://mohanadarafe.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        LIMIT = int(self.limit)
        PATH = "spiders/test_results"
        if not os.path.isdir(PATH):
            os.makedirs(PATH)
        else:
            shutil.rmtree(PATH)
            os.makedirs(PATH)

        links = self.extractor.extract_links(response)
        for index, link in enumerate(links):
            yield scrapy.Request(url = link.url, callback=self.parse_links)

    def parse_links(self, response):
        LIMIT = int(self.limit)
        if len(os.listdir('spiders/test_results')) < LIMIT:
            with open(f'spiders/test_results/{self.linkNumber}.html', 'wb') as f:
                f.write(response.body)
            self.linkNumber += 1