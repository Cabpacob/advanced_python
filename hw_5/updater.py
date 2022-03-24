from page_getter import PageGetter
from bs4 import BeautifulSoup
from offer import ShortOffer
import asyncio


class Updater:
    def __init__(self, database):
        self.__urls = dict()
        self.__database = database

    def register(self, city='sankt-peterburg', action='snyat', realty='kvartira'):
        url = f'https://realty.yandex.ru/{city}/{action}/{realty}/?from=main_menu&sort=DATE_DESC'
        assert url not in self.__urls
        self.__urls[url] = (city, action, realty)

    async def __get_new_short_offers(self, url):
        offers = []
        html_text = await PageGetter.get_page(url, cached=False)

        soup = BeautifulSoup(html_text, 'lxml')

        l = soup.find_all('ol')
        for tag in l[1].find_all('li'):

            if len(tag.find_all('a')) > 0:
                kwargs = dict()
                kwargs['href'] = 'https://realty.yandex.ru' + tag.find_all('a')[0].get('href')
                kwargs['offer_id'] = kwargs['href'].split('/')[4]

                if not await self.__database.is_new_offer(kwargs['offer_id']):
                    continue

                await self.__database.register_new_short_offer(kwargs['offer_id'], kwargs['href'])

                kwargs['city'], kwargs['action'], kwargs['realty'] = self.__urls[url]

                kwargs['price'] = tag.find(class_='Price OffersSerpItem__price').text

                kwargs['image_ref'] = 'https://' + tag.find_all('img')[0].get('srcset').split(', ')[-1].split(' ')[0][2:]
                kwargs['size'] = tag.find_all('h3')[0].text
                kwargs['location'] = tag.find_all(class_='OffersSerpItem__building')[0].text
                kwargs['address'] = tag.find_all(class_='OffersSerpItem__address')[0].text

                kwargs['closest_metro_name'] = tag.find_all(class_='MetroStation__title')[0].text
                kwargs['closest_metro_dist'] = tag.find_all(class_='MetroWithTime__distance')[0].text
                kwargs['closest_metro_dist_type'] = tag.find_all(class_='MetroWithTime__distance')[0].find('i').get('class')[-1].split('-')[-1]

                kwargs['payments_info'] = tag.find_all(class_='ItemPaymentsInfo OffersSerpItem__paymentsInfo')[0].text

                kwargs['short_description'] = tag.find_all(class_='OffersSerpItem__description')[0].text

                for key, value in kwargs.items():
                    if type(value) == str:
                        kwargs[key] = value.replace('\xa0', ' ')

                offers.append(kwargs)
                break
        return offers

    async def get_new_short_offers(self):
        tasks = [
            asyncio.create_task(self.__get_new_short_offers(url))
            for url in self.__urls.keys()
        ]
        offers = await asyncio.gather(*tasks)
        if len(offers[0]) == 0:
            return []
        return list(map(lambda offer: ShortOffer(**offer[0]), offers))
