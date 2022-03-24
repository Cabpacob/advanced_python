from telebot.async_telebot import AsyncTeleBot
from telebot import types
from database import UserConfig
from collections import defaultdict
import asyncio


class Bot:
    def __init__(self, database):
        self.__database = database
        token = ''
        self.__bot = AsyncTeleBot(token)
        self.__init__handlers()
        self.__updated_users = defaultdict(lambda: '')

    def __init__handlers(self):
        help_message = '\n'.join([
            'Я помогу тебе найти объявление в Санкт-Петербурге, которое тебе нужно',
            '',
            '<b>Мной можно управлять с помощью следующих команд</b>',
            '/help - выводит сообщение с помощью',
            '/filters - показывает текущие фильтры',
            '/editfilters - позволяет поменять параметры поиска (по умолчанию показываются все объявления)',
        ])

        @self.__bot.message_handler(commands=['start'])
        async def start(message):
            await self.__database.add_new_user_config(UserConfig(message.chat.id))
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f'Привет!\n{help_message}',
                parse_mode='HTML'
            )
            self.__updated_users[message.chat.id] = ''

        @self.__bot.message_handler(commands=['help'])
        async def help(message):
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f'{help_message}',
                parse_mode='HTML'
            )
            self.__updated_users[message.chat.id] = ''

        @self.__bot.message_handler(commands=['filters'])
        async def filters(message):
            config = await self.__database.get_user_config(message.chat.id)
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=f'{config.html()}',
                parse_mode='HTML'
            )
            self.__updated_users[message.chat.id] = ''

        @self.__bot.message_handler(commands=['editfilters'])
        async def edit_filters(message):
            text = '\n'.join([
                'Введи 1, если хочешь поменять нижнюю границу цены',
                'Введи 2, если хочешь поменять верхнюю границу цены',
                'Введи 3, если хочешь поменять ближайшую станцию метро'
            ])

            self.__updated_users[message.chat.id] = 'choice'
            await self.__bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode='HTML'
            )

        @self.__bot.message_handler(func=lambda message: self.__updated_users[message.chat.id] == 'choice', content_types=['text'])
        async def choose_type(message):
            texts = ['1', '2', '3']

            if message.text not in texts:
                await self.__bot.send_message(
                    chat_id=message.chat.id,
                    text='Неправильная цифра, попробуй еще раз',
                    parse_mode='HTML'
                )
                return

            self.__updated_users[message.chat.id] = message.text
            if message.text in ['1', '2']:
                await self.__bot.send_message(
                    chat_id=message.chat.id,
                    text='Введи сумму одним числом без пробелов или delete чтобы удалить этот фильтр',
                    parse_mode='HTML'
                )
            else:
                await self.__bot.send_message(
                    chat_id=message.chat.id,
                    text='Введи название станции метро или delete чтобы удалить этот фильтр',
                    parse_mode='HTML'
                )

        @self.__bot.message_handler(func=lambda message: self.__updated_users[message.chat.id] in ['1', '2', '3'], content_types=['text'])
        async def update_config(message):
            if message.text == 'delete':
                config = await self.__database.get_user_config(message.chat.id)
                if self.__updated_users[message.chat.id] == '1':
                    config.price_from = None
                elif self.__updated_users[message.chat.id] == '2':
                    config.price_to = None
                else:
                    config.closest_metro = None
                await self.__database.set_user_config(config)
                await self.__bot.send_message(
                        chat_id=message.chat.id,
                        text='Фильтры обновлены',
                        parse_mode='HTML'
                    )
                return

            if self.__updated_users[message.chat.id] in ['1', '2']:
                print(message.text)
                try:
                    number = int(message.text)
                except Exception:
                    await self.__bot.send_message(
                        chat_id=message.chat.id,
                        text='Неверное число, попробуй еще раз',
                        parse_mode='HTML'
                    )
                    return
                config = await self.__database.get_user_config(message.chat.id)
                print(config)
                if self.__updated_users[message.chat.id] == '1':
                    config.price_from = str(number)
                elif self.__updated_users[message.chat.id] == '2':
                    config.price_to = str(number)

                await self.__database.set_user_config(config)
                await self.__bot.send_message(
                        chat_id=message.chat.id,
                        text='Фильтры обновлены',
                        parse_mode='HTML'
                )
            else:
                name = message.text
                config = await self.__database.get_user_config(message.chat.id)
                config.closest_metro = name
                await self.__database.set_user_config(config)
                await self.__bot.send_message(
                        chat_id=message.chat.id,
                        text='Фильтры обновлены',
                        parse_mode='HTML'
                    )

    async def handle_new_short_offers(self, offers):
        for offer in offers:
            image = await offer.get_image().open()
            try:
                image.caption = f'<b>Новое предложение для тебя</b>\n\n{offer}'
                image.parse_mode = 'HTML'
                users = await self.__database.get_users_by_short_offer(offer)

                for user in users:
                    await self.__bot.send_photo(
                        chat_id=user,
                        photo=image,
                        caption = f'<b>Новое предложение для тебя</b>\n\n{offer}',
                        parse_mode = 'HTML',
                        reply_markup=types.InlineKeyboardMarkup([
                            [types.InlineKeyboardButton(text='Перейти к объявлению', url=offer.href)],
                        ])
                    )
            except Exception:
                pass
            finally:
                await image.close()


    async def do_work(self):
        # print('I do work')
        # while True:
        await self.__bot.polling(none_stop=True)
        # await asyncio.sleep(1)
        # print('I undo work')

