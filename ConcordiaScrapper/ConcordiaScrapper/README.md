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
The crawler will go get a number of links from [Concordia's](https://www.concordia.ca/) website & store the HTML file inside `spider/concordia_results`.

```
scrapy crawl concordia -a limit=100

limit: upper bound on the number of files to download
```
