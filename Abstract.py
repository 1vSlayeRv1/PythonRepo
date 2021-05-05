import abc
import requests
import datetime
import json
import asyncio
import aiohttp


def timer(requests):
    def my_func(func):
        def wrapper(self, url, filename):
            print("Запуск синхронной функции(метода)")
            time = datetime.datetime.now()
            for i in range(requests):
                func(self, url, filename, i)
                print(f"Create file \"{filename}_{i}.jpg\"")
            print("Время выполнения:", datetime.datetime.now() - time)

        return wrapper

    return my_func


def async_timer(requests):
    def my_func(func):
        def wrapper(self, url, filename, logging):
            print("Запуск асинхронной функции(метода)")
            time = datetime.datetime.now()
            func(self, url, filename, requests, logging)

            print("Время выполнения:", datetime.datetime.now() - time)

        return wrapper

    return my_func


class Download_images(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def download_image(self, url, filename, counter):
        content = requests.get(url)
        content = content.content.decode()
        content = json.loads(content)
        image = requests.get(content['file'])
        image = image.content
        with open(f"{filename}_{counter}.jpg", 'wb') as f:
            f.write(image)

    async def requests_(self, url, filename, session, require_number):
        url = "https://aws.random.cat/meow"
        async with session.get(url) as resp:
            if resp.status == 200:
                return json.loads(await resp.text())

    async def downloads_(self, url, filename, session, require_number, logging):
        images = await self.requests_(url, filename, session, require_number)
        async with session.get(images['file']) as resp2:
            with open(f"{filename}_async_{require_number}.jpg", 'wb') as f:
                f.write(await resp2.read())
                if logging:
                    print(f"Create file \"{filename}_async_{require_number}.jpg\"")

    async def main(self, url, filename, val, logging):
        number_req = val
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                *[self.downloads_(url, filename, session, i, logging) for i in range(number_req)],
            )

    @abc.abstractmethod
    def async_many_downloads(self, url, filename, val, logging=False):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main(url, filename, val, logging))


class Download_sync(Download_images):
    @timer(5)
    def download_image(self, url, filename, counter):
        super().download_image(url, filename, counter)

    @async_timer(5)
    def async_many_downloads(self, url, filename, val, logging):
        super().async_many_downloads(url, filename, val, logging)


ds = Download_sync()
ds.download_image("https://aws.random.cat/meow", "cat")
ds.async_many_downloads("https://aws.random.cat/meow", "catA", logging=True)
