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

### 1. Test Crawler
Before starting to crawl the Concordia website, I decided to test Scrapy on my portfolio website. The crawler will go get a number of links from [my website](http://www.mohanadarafe.com/) & build an inverted index. To run the test, simple execute the following command:

```
python test.py
```

### 2. Concordia Crawler
The crawler will go get a number of links from [Concordia's](https://www.concordia.ca/) website & build an inverted index.

```
python run.py
```

### 3. Query
**Once you crawled the domain** you can run a query of your choice.

```
python query.py
```