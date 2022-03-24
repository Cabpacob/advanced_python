import os
import aiofiles
from image_downloader import AsyncImageDownloader
from telebot.types import InputMediaPhoto
import asyncio


class ShortOffer:
    def __init__(
        self,
        href,
        offer_id,
        city,
        action,
        realty,
        price,
        image_ref,
        size,
        location,
        address,
        closest_metro_name,
        closest_metro_dist,
        closest_metro_dist_type,
        payments_info,
        short_description
    ):
        self.href = href
        self.offer_id = offer_id
        self.city = city
        self.action = action
        self.realty = realty
        self.price = price
        self.image_ref = image_ref
        self.size = size
        self.location = location
        self.address = address
        self.closest_metro_name = closest_metro_name
        self.closest_metro_dist = closest_metro_dist
        self.closest_metro_dist_type = closest_metro_dist_type
        assert closest_metro_dist_type in ['bus', 'pedestrian']

        self.payments_info = payments_info
        self.short_description = short_description

    def __str__(self):
        map_realty = {
            'kvartira': 'Квартира'
        }

        map_metro_dist_type = {
            'bus': 'на транспорте',
            'pedestrian': 'пешком'
        }

        return '\n'.join([
            f'<b>Краткая информация</b>',
            f'{self.size} по адресу {self.address}',
            f'{self.location}',
            '',
            '<b>Стоимость</b>',
            f'{self.price}',
            '',
            '<b>Ближайшая станция метро</b>',
            f'{self.closest_metro_name}, {self.closest_metro_dist} {map_metro_dist_type[self.closest_metro_dist_type]}',
            '',
            f'<b>Информация об оплате</b>\n{self.payments_info}',
            '',
            f'<b>Краткое описание от владельца (может быть обрезано)</b>\n{self.short_description}'
        ])

    def get_image(self):
        image_ref = self.image_ref
        offer_id = self.offer_id

        class ShortOfferImage:
            __prefix = 'images/'

            async def open(self):
                self.__path = os.path.join(self.__prefix, f'{offer_id}_0')
                await AsyncImageDownloader.download_image(image_ref, self.__path)
                self.__file = await aiofiles.open(self.__path, 'rb')
                return self.__file

            async def close(self):
                await self.__file.close()
                os.remove(self.__path)

        return ShortOfferImage()
