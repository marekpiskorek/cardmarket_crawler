# Cardmarket crawler #

### Disclaimer:

This project assumes that it's users understand the basics of web crawling with scrapy (or are willing to learn). As complicated as it might be for people with no experience for now, I will try to simplify the usage and improve on providing all the instructions necessary.

#### Motivation:

Cardmarket is by far the best option for buying cards to such popular TCGs as Magic: the Gathering (plus much more, but I don't really care for other games). However, the main problem remains in poor UX in terms of browsing for completing a deck or cube. With my crawler I intend to overpass this obstacle and prepare a solution of my own, that will not harm cardmarket but even increase its usability (and, potentially, its revenue).

#### Workplan:

First off, I am starting with bulk searches on my favourite seller in order to check if my needs are met with his resources.

Secondly I would like to search for cards from the same source (a file with decklist) but among all possible sellers in order to combine the most optimal sale (think ChannelFireball store bulk search but for multiple sellers). This is indeed a though one and will require some advanced data analysis.

#### Means (all necessary):

I'm using scrapy + splash for AJAX load of results table content.
Set of user agents is in preparation. I will test this on TOR connections, if it won't work (or won't be fast enough) I'll need to move to a proxy pool, hopefully a free one as my goal here is to seek optimal buys in order to *save* money.

### Install:

Splash installation for scrapy can be found [here](https://github.com/scrapy-plugins/scrapy-splash#installation). Spoiler alert: it's easily done with Docker.

*Tha crawler:* `pip install -r requirements.txt`

### Run:

1. Add your decklist / whatever into `CARD_LIST` variable in `cardmarket/spiders/cardmarket.py` (`TODO`: a file) It handles amounts set et the beginning of each line, default is `1`. Possible input formats are:

> 2x Fumigate

> 3 Settle the Wreckage

> Chromatic Lantern

2. Run splash and set its host/port in crawler settings (under `SPLASH_URL`, remember the `http(s)` prefix)
3. Run the crawler: `scrapy crawl cardmarket`

### Development:

I will try to handle below ASAP, regarding the following TODO list:

* check & implement TOR for anonymous calls
* Check the expected amount versus found amount (and present bool flag for this)
* Examine expected name vs found name, skip if those doesn't match
* parse price in order to present total price on found cards (with regard to expected amount)
* present results in JSON file / HTML report
* add card comments to results
* prepare login function for possibility of auto-adding to basket & return link to check basket and buy
* implement the all-sellers feature with configurable reports on top N possible buys
