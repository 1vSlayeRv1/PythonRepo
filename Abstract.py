import abc
import requests
import datetime
import json
import asyncio
import aiohttp


def timer(val):
    def my_func(func):
        def wrapper(self, url, filename):
            print("Запуск синхронной функции(метода)")
            time = datetime.datetime.now()
            for i in range(val):
                func(self, url, filename, i)
                print(f"Create file \"{filename}_{i}.jpg\"")
            print("Время выполнения:", datetime.datetime.now() - time)

        return wrapper

    return my_func


def async_timer(val):
    def my_func(func):
        def wrapper(self, url, filename):
            print("Запуск асинхронной функции(метода)")
            time = datetime.datetime.now()
            func(self, url, filename, val, True)

            print("Время выполнения:", datetime.datetime.now() - time)

        return wrapper

    return my_func


class AbstractDownload(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def download_images_sync(self, url, filename, val):
        pass

    async def get_url_img(self, url, filename, session, require_number):
        url = "https://aws.random.cat/meow"
        async with session.get(url) as resp:
            if resp.status == 200:
                return json.loads(await resp.text())

    async def download_img(self, url, filename, session, require_number, logging):
        images = await self.get_url_img(url, filename, session, require_number)
        async with session.get(images['file']) as resp2:
            with open(f"{filename}_async_{require_number}.jpg", 'wb') as f:
                f.write(await resp2.read())
                if logging:
                    print(f"Create file \"{filename}_async_{require_number}.jpg\"")

    async def main(self, url, filename, val, logging):
        number_req = val
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                *[self.download_img(url, filename, session, i, logging) for i in range(number_req)],
            )

    @abc.abstractmethod
    def async_many_downloads(self, url, filename, val, logging=False):
        pass


class Download(AbstractDownload):
    @timer(5)
    def download_images_sync(self, url, filename, val):
        content = requests.get(url)
        content = content.content.decode()
        content = json.loads(content)
        image = requests.get(content['file'])
        image = image.content
        with open(f"{filename}_{val}.jpg", 'wb') as f:
            f.write(image)

    @async_timer(5)
    def async_many_downloads(self, url, filename, val, logging):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main(url, filename, val, logging))


download_img = Download()
download_img.download_images_sync("https://aws.random.cat/meow", "cat")
download_img.async_many_downloads("https://aws.random.cat/meow", "cat")
