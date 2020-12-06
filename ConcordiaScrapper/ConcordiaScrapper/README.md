# Concordia Scrapper

## Objective
Experiment with web crawling, scrape and index a set of web documents, use the sentiment dictionary aFinn to associate sentiment values to the index, make document ranking reflect sentiment.

### Setup
Make sure you have Conda installed on your machine
```
conda env create --name scrapper --file=environment.yml
conda activate scrapper
```

### Run
You can run the crawler using the following command:
```
scrapy crawl test -a limit=100

limit: upper bound on the number of files to download
```
