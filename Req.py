import requests
import datetime
import json
import asyncio
import aiohttp


def timer(func):
    def wrapper(val):
        time = datetime.datetime.now()
        func(val)
        print(datetime.datetime.now() - time)

    return wrapper


def download_image(url, filename):
    content = requests.get(url)
    content = content.content.decode()
    content = json.loads(content)
    image = requests.get(content['file'])
    image = image.content
    with open(f"{filename}.jpg", 'wb') as f:
        f.write(image)


@timer
def many_downloads(val):
    for i in range(val):
        download_image('https://aws.random.cat/meow', f'cat_{i}.jpg')


async def req(session, require_number):
    url = "https://aws.random.cat/meow"
    async with session.get(url) as resp:
        if resp.status == 200:
            return json.loads(await resp.text())


async def downl(session, require_number):
    images = await req(session, require_number)
    async with session.get(images['file']) as resp2:
        with open(f"cat_async_{require_number}.jpg", 'wb') as f:
            f.write(await resp2.read())


async def main(val):
    number_req = val
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[downl(session, i) for i in range(number_req)],
        )


@timer
def async_many_downloads(val):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(val))


print("Синхронная загрузка:")
many_downloads(5)
print("Асинхронная загрузка:")
async_many_downloads(5)
