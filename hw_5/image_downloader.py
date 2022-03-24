import aiohttp
import asyncio
import aiofiles


class AsyncImageDownloader:
    @classmethod
    async def __download_image(cls, url, session, path):
        async with session.get(url) as responce:
            async with aiofiles.open(path, 'wb') as f:
                await f.write(await responce.read())

    @classmethod
    async def __download(cls, urls, paths):
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(
                    cls.__download_image(
                        url,
                        session,
                        path
                    )
                )
                for url, path in zip(urls, paths)
            ]
            await asyncio.gather(*tasks)

    @classmethod
    async def download_image(cls, url, path):
        await cls.__download([url], [path])

    @classmethod
    async def download_album(cls, urls, paths):
        await cls.__download(urls, paths)
