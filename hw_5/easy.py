import aiohttp
import asyncio
import aiofiles
import os
import sys


async def download_image(url, session, path):
    async with session.get(url) as responce:
        async with aiofiles.open(path, 'wb') as f:
            await f.write(await responce.read())


async def main(folder, images_number):
    url = 'https://picsum.photos/200/300'
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(
                download_image(
                    url,
                    session,
                    os.path.join(folder, f'image_{i + 1}.jpg')
                )
            )
            for i in range(images_number)
        ]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    folder, images_number = sys.argv[1:]
    images_number = int(images_number)
    asyncio.run(main(folder, images_number))
