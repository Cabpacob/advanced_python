import asyncpg
import asyncio


class UserConfig:
    def __init__(self, user_id, price_from=None, price_to=None, closest_metro=None):
        self.user_id = user_id
        self.city='Санкт-Петербург' #TODO
        self.price_from = price_from
        self.price_to = price_to
        self.closest_metro = closest_metro

    def __bool__(self):
        return bool(self.price_from or self.price_to or self.closest_metro)

    def __str__(self):
        l = [str(self.user_id)]

        l.append('\'sankt-peterburg\'')
        if self.price_from:
            l.append(f'{self.price_from}')
        else:
            l.append('NULL')

        if self.price_to:
            l.append(f'{self.price_to}')
        else:
            l.append('NULL')

        if self.closest_metro:
            l.append(f'\'{self.closest_metro}\'')
        else:
            l.append('NULL')
        return '(' + ', '.join(l) + ')'

    def html(self):
        if not self:
            return 'У тебя нет активных фильтров, показываются все объявления в Санкт-Петербурге'

        s = ''

        if self.price_from:
            s += f'Цена от {self.price_from}\n'

        if self.price_to:
            s += f'Цена до {self.price_to}\n'

        if self.closest_metro:
            s += f'Ближайшая станция метро {self.closest_metro}\n'
        return f'<b>Активные фильтры</b>\n{s}'

    def as_dict_str(self):
        l = []

        if self.price_from:
            l.append(f'price_from = {self.price_from}')
        else:
            l.append('price_from = NULL')

        if self.price_to:
            l.append(f'price_to = {self.price_to}')
        else:
            l.append('price_to = NULL')

        if self.closest_metro:
            l.append(f'closest_metro = \'{self.closest_metro}\'')
        else:
            l.append('closest_metro = NULL')
        return ', '.join(l)

class Database:
    def __init__(self):
        pass

    async def create_tables(self):
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS UserConfigs (
                    id BIGINT PRIMARY KEY,
                    city TEXT NOT NULL,
                    price_from MONEY,
                    price_to MONEY,
                    closest_metro TEXT
                );
            '''
         )

        await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS ShortOffers (
                    id BIGINT PRIMARY KEY,
                    url TEXT NOT NULL
                );
            '''
        )

    async def register_new_short_offer(self, offer_id, url):
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        await connection.execute(
            '''
                INSERT INTO ShortOffers
                VALUES ({offer_id}, \'{url}\')
            '''.format(offer_id=offer_id, url=url)
        )

    async def is_new_offer(self, offer_id):
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        result = await connection.fetch(
            '''
                SELECT id FROM ShortOffers
                WHERE id = {offer_id}
            '''.format(offer_id=offer_id)
        )
        return len(result) == 0

    async def get_user_config(self, user_id):
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        tpl = await connection.fetch(
            '''
                SELECT * FROM UserConfigs
                WHERE id = {user_id}
            '''.format(user_id=user_id)
        )
        tpl = dict(tpl[0])
        config = dict()
        config['user_id'] = tpl['id']
        config['price_from'] = tpl['price_from']
        config['price_to'] = tpl['price_to']
        config['closest_metro'] = tpl['closest_metro']

        return UserConfig(**config)

    async def add_new_user_config(self, config):
        if config.price_from:
            config.price_from = int(config.price_from.split(',')[0])
        if config.price_to:
            config.price_to = int(config.price_to.split(',')[0])

        print(config)
        user_id = config.user_id
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        await connection.execute(
            '''
                INSERT INTO UserConfigs
                VALUES {config}
                ON CONFLICT DO NOTHING
            '''.format(user_id=user_id, config=f'{config}')
        )

    async def set_user_config(self, config):
        if config.price_from:
            config.price_from = int(config.price_from.split(',')[0])
        if config.price_to:
            config.price_to = int(config.price_to.split(',')[0])
        user_id = config.user_id
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        await connection.execute(
            '''
                UPDATE UserConfigs
                SET {config}
                WHERE id = {user_id}
            '''.format(user_id=user_id, config=config.as_dict_str())
        )

    async def get_users_by_short_offer(self, short_offer):
        connection = await asyncpg.connect(database='yandex_realty_bot_db', user='yandex_realty_bot', host='localhost', password='botbot')
        result = await connection.fetch(
            '''
                SELECT id FROM UserConfigs
                WHERE (price_from is NULL or price_from <= {price}::MONEY)
                  and (price_to is NULL or price_to >= {price}::MONEY)
                  and (closest_metro is NULL or closest_metro = \'{closest_metro}\')
            '''.format(price=int(short_offer.price.split('₽')[0].replace(' ', '')), closest_metro=short_offer.closest_metro_name)
        )
        return list(map(lambda res: res.get('id'), result))
