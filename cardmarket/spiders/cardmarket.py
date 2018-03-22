from collections import defaultdict
from pprint import pprint

import scrapy

from scrapy_splash import SplashRequest


CARDMARKET_URL = (
    'https://www.cardmarket.com/en/Magic/MainPage/browseUserProducts?'
    'idCategory=1&idUser=54710&resultsPage=0&cardName={}&idLanguage=0'
    '&isFoil=0&isSigned=0&isPlayset=0&isAltered=0'
)

# Example list of cards to parse
CARD_LIST = """
1x Hellkite Overlord
3 Glorybringer
Sacred Cat

"""


class CardMarketSpider(scrapy.Spider):
    name = 'cardmarket'

    def start_requests(self):
        self.prepare_input_data()
        for card_name, amount in self.input_data.items():
            card_name = card_name.replace(' ', '%20')
            url = CARDMARKET_URL.format(card_name)
            yield SplashRequest(
                url=url, callback=self.parse, args={'wait': 1}, meta={'card_name': card_name},
            )

    def prepare_input_data(self):
        self.input_data = {}
        for element in CARD_LIST.split('\n'):
            if not element.strip():
                continue
            card_name, amount = self._parse_input_line(element)
            self.input_data[card_name] = amount
        self.results = defaultdict(list)

    def _parse_input_line(self, element):
        try:
            int(element[0])  # if this breaks this means that the line doesn't start with a number
            element_words = element.split(' ')
            amount = element_words[0]
            if 'x' in amount:
                amount = amount[:-1]  # I assume for of 4x cardname, not x4 cardname
            amount = int(amount)
            card_name = element_words[1:]
            card_name = ' '.join(card_name)
        except (ValueError, IndexError):  # It has no card amount in it
            amount = 1
            card_name = element
        return card_name, amount

    def parse(self, response):
        for result in response.xpath(
            '//*[@id="bupPaginator.innerNavBarCodeDiv"]/table/tbody/tr'
        ):
            expected_card_name = response.request.meta['card_name']
            title = result.css('.vAlignMiddle div a::text').extract_first()
            if title.lower() != expected_card_name.lower():
                # name mismatch, perform further checks and consider skipping this response
                pass
            foil = result.css('.centered').css('.nowrap span::attr(onmouseover)').extract_first() is not None
            pic_url, edition, rarity, language, condition = self.get_onmouseovers(result)
            price = result.css('.st_price div::text').extract_first()
            amount = result.css('.st_ItemCount::text').extract_first()
            # TODO: add comment and real photo url
            data = {
                'pic_url': pic_url,  # to see the picture add https://www.cardmarket.com/
                'edition': edition,
                'rarity': rarity,
                'language': language,
                'condition': condition,
                'foil': foil,
                'price': price,
                'amount': int(amount),
            }
            pprint(data)
            self.results[title].append(data)

    def get_onmouseovers(self, result):
        for element in result.css('.centered span::attr(onmouseover)').extract()[:5]:
            yield element.split("'")[1]
