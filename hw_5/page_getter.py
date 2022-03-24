from requests_html import AsyncHTMLSession
from os import path
from hashlib import md5
import aiofiles
from fake_headers import Headers


class PageGetter:
    __prefix = 'htmls/'

    @staticmethod
    def __get_hash(url):
        return md5(url.encode()).hexdigest()

    @classmethod
    def __get_path(cls, url):
        h = cls.__get_hash(url)
        return path.join(cls.__prefix, f'{h}.html')

    @classmethod
    async def get_cached(cls, url):
        async with aiofiles.open(cls.__get_path(url), 'r') as f:
            html = await f.read()
        return html

    @classmethod
    async def get_uncached(cls, url):
        session = AsyncHTMLSession()
        responce = await session.get(url)
        await responce.html.arender(timeout=20)
        html_text = responce.html.html
        h = cls.__get_hash(url)
        async with aiofiles.open(cls.__get_path(url), 'w') as f:
            await f.write(html_text)
        return html_text

    @classmethod
    async def get_page(cls, url, cached=False):
        if cached:
            return await cls.get_cached(url)
        else:
            return await cls.get_uncached(url)
