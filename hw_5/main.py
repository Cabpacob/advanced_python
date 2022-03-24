from database import Database
from bot import Bot
from updater import Updater
from multiprocessing import Process
import time
import asyncio


async def offers_loop(bot, updater):
    while True:
        new_short_offers = await updater.get_new_short_offers()
        await bot.handle_new_short_offers(new_short_offers)
        await asyncio.sleep(60)


async def main():
    database = Database()
    await database.create_tables()
    updater = Updater(database)
    updater.register()
    bot = Bot(database)

    tasks = [
        asyncio.create_task(bot.do_work()),
        asyncio.create_task(offers_loop(bot, updater))
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

# from datetime import datetime

# import logging
# import re
# import time
# import traceback
# from typing import Any, List, Optional, Union

# this imports are used to avoid circular import error
# import telebot.util
# import telebot.types


# storages
# from telebot.asyncio_storage import StateMemoryStorage, StatePickleStorage
# from telebot.asyncio_handler_backends import CancelUpdate, SkipHandler

# from inspect import signature

# from telebot import logger

# import asyncio
# from telebot import asyncio_filters

# from telebot import asyncio_helper
# import aiohttp
# import asyncio


# async def main():
#     c = aiohttp.ClientSession()
#     await c.close()


# if __name__ == '__main__':
#     asyncio.run(main())