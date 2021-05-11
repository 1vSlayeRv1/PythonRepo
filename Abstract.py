import abc
import datetime
import json
import requests
import typing
# from __future__ import annotations

import asyncio
import aiohttp


def timer(func_type: str, is_logging: bool = False):
    def my_func(func):
        def wrapper(self, url: str, filename: str, value_requests: int):
            if func_type == "sync":
                print("Запуск синхронной функции(метода)")
                started_at = datetime.datetime.now()
                for i in range(value_requests):
                    func(self, url, filename, i)
                    if is_logging:
                        print(f"Create file \"{filename}_{i}.jpg\"")
                print("Время выполнения:",
                      datetime.datetime.now() - started_at)

            elif func_type == "async":
                print("Запуск асинхронной функции(метода)")
                started_at = datetime.datetime.now()
                func(self, url, filename, value_requests, is_logging)
                print("Время выполнения:",
                      datetime.datetime.now() - started_at)
            elif func_type == "txt":
                print("Запуск функции загрузки данных сайта в txt")
                started_at = datetime.datetime.now()
                func(self, url, filename, value_requests, is_logging)
                print("Время выполнения:",
                      datetime.datetime.now() - started_at)

        return wrapper

    return my_func


class AbstractDownload(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def get_info_from_url(self, *args, **kwargs) -> typing.Any:
        pass

    @abc.abstractmethod
    async def downloader(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    async def main(self, *args, **kwargs) -> None:
        pass


class DownloadImgSync(AbstractDownload):
    @timer("sync", True)
    def __init__(self, url: str, filename: str, image_counter: int = 1):
        self.main(url, filename, image_counter)

    def get_info_from_url(self, url: str) -> dict[str, str]:
        response = requests.get(url)
        response_decode = response.content.decode()
        response_json = json.loads(response_decode)
        return response_json

    def downloader(self, url: str, filename: str, image_counter: int) -> None:
        image = requests.get(self.get_info_from_url(url)['file'])
        with open(f"{filename}_{image_counter}.jpg", 'wb') as f:
            f.write(image.content)

    def main(self, url: str, filename: str, image_counter: int) -> None:
        self.downloader(url, filename, image_counter)


class DownloadImgAsync(AbstractDownload):
    @timer("async", True)
    def __init__(self, url: str, filename: str,
                 value_requests: int = 1, is_logging: bool = False):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.main(url, filename, value_requests, is_logging))

    async def get_info_from_url(self, url: str, session) -> dict[str, str]:
        async with session.get(url) as resp:
            if resp.status == 200:
                return json.loads(await resp.text())
            else:
                raise requests.exceptions.HTTPError

    async def downloader(self, url: str, filename: str,
                         session, require_number: int,
                         is_logging: bool) -> None:
        images = await self.get_info_from_url(url, session)
        async with session.get(images['file']) as resp2:
            with open(f"{filename}_async_{require_number}.jpg", 'wb') as f:
                f.write(await resp2.read())
                if is_logging:
                    print(
                        f"Create file \"{filename}"
                        f"_async_{require_number}.jpg\"")

    async def main(self, url: str, filename: str, value_requests: int,
                   is_logging: bool) -> None:
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                *[self.downloader(url, filename, session, i, is_logging) for i
                  in
                  range(value_requests)],
            )


class DownloadTxt(AbstractDownload):
    @timer("txt", True)
    def __init__(self, url: str, filename: str, value_requests: int = 1,
                 is_logging: bool = False):
        self.url = url
        self.value_requests = value_requests
        self.filename = filename
        self.is_logging = is_logging

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

    async def get_info_from_url(self, *args, **kwargs) -> str:
        async with args[0].get(self.url) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                raise requests.exceptions.HTTPError

    async def main(self, *args, **kwargs) -> None:
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                *[self.downloader(session, i) for i in
                  range(self.value_requests)]
            )

    async def downloader(self, *args, **kwargs) -> None:
        """

        :param args: (session, file_counter)
        """
        txt = await self.get_info_from_url(args[0])
        with open(f'{self.filename}_{args[1]}.txt', 'w') as f:
            f.write(txt)
            if self.is_logging:
                print(f'file \"{self.filename}_{args[1]}.txt\" created')


CAT_API_URL = "https://aws.random.cat/meow"

DownloadTxt(CAT_API_URL, "json_from_aws", 2)

DownloadImgAsync(CAT_API_URL, "cat", 5)

DownloadImgSync(CAT_API_URL, "cat", 5)
