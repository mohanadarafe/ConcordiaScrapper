import os, shutil
from scrapy.crawler import CrawlerProcess
from spiders.test_crawler import TestScrapper

upperBound = input("Please enter an upper bound: ")
while (not upperBound.isnumeric() or int(upperBound) < 0):
    print("Invalid input. Please enter a positive number.")
    upperBound = input("Please enter an upper bound: ")

if os.path.isdir("results"):
        shutil.rmtree("results")

os.makedirs("results")
os.chdir("results")

process = CrawlerProcess(settings={
    "CONCURRENT_REQUESTS": 1,
    "ROBOTSTXT_OBEY": True,
    "CLOSESPIDER_ITEMCOUNT": upperBound,
    "LOG_LEVEL": "INFO",
    "FEEDS": {
        'test_result.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False
        },
    },
})
TestScrapper.file_limit = upperBound
process.crawl(TestScrapper)
process.start()