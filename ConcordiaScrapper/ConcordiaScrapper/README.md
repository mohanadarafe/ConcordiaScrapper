# Concordia Scrapper

## Objective
Experiment with web crawling, scrape and index a set of web documents, use the sentiment dictionary aFinn to associate sentiment values to the index, make document ranking reflect sentiment.

## Setup
Make sure you have Conda installed on your machine
```
conda env create --name scrapper --file=environment.yml
conda activate scrapper
```

## Run
The following commands are used to run different parts of the scrapper.

### Crawler
The crawler will go get a number of links from [Concordia's](https://www.concordia.ca/) website & build an inverted index.

```
python run.py
```

If you want to run the test file I have that parses my personal website:
```
scrapy crawl test -a limit=15

limit: upper bound on the number of files to download
```
