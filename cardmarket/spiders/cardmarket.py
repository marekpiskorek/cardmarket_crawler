from collections import defaultdict
from pprint import pprint

import scrapy

from scrapy_splash import SplashRequest


url = (
    'https://www.cardmarket.com/en/Magic/MainPage/browseUserProducts?'
    'idCategory=1&idUser=54710&resultsPage=0&cardName={}&idLanguage=0'
    '&isFoil=0&isSigned=0&isPlayset=0&isAltered=0'
)

# Example list of cards to parse
CARD_LIST = """
1x Hellkite Overlord
3 Glorybringer
Sacrded Cat

"""


class CardMarketSpider(scrapy.Spider):
    name = 'cardmarket'
    results = defaultdict(list)

    def _get_urls(self):
        for element in CARD_LIST.split('\n'):
            if not element:
                continue
            try:
                int(element[0])
                passable = element.split(' ')[1:]
                element = ' '.join(passable)
            except ValueError:
                # It has no card amounts in it
                pass
            card_name = element.replace(' ', '%20')
            yield url.format(card_name)

    def start_requests(self):
        for url in self._get_urls():
            yield SplashRequest(
                url=url, callback=self.parse, args={'wait': 1}
            )

    def parse(self, response):
        for result in response.xpath(
            '//*[@id="bupPaginator.innerNavBarCodeDiv"]/table/tbody/tr'
        ):
            title = result.css('.vAlignMiddle div a::text').extract_first()
            import ipdb; ipdb.set_trace()
            foil = result.css('.centered').css('.nowrap span::attr(onmouseover)').extract_first() is not None
            pic_url, edition, rarity, language, condition = self.get_onmouseovers(result)
            price = result.css('.st_price div::text').extract_first()
            amount = result.css('.st_ItemCount::text').extract_first()
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
        for element in result.css('.centered span::attr(onmouseover)').extract():
            yield element.split("'")[1]
