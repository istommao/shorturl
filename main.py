# coding: utf-8

from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import aioredis
import mmh3

app = FastAPI()


REDIS_CONFIG = ('127.0.0.1', 6379)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Item(BaseModel):
    url: str


def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


def get_short_url_code(url):
    hash_num = mmh3.hash(url)
    code = base62_encode(abs(hash_num))

    return code


class Redis:
    _redis = None

    async def get_redis_pool(self, *args, **kwargs):
        if not self._redis:
            self._redis = await aioredis.create_redis_pool(*args, **kwargs)
        return self._redis

    async def close(self):
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()


async def get_value(key):
    redis = Redis()
    r = await redis.get_redis_pool(('127.0.0.1', 6379), db=0, encoding='utf-8')

    value = await r.get(key)
    await redis.close()
    return value


async def set_value(key, value, expire=None):
    redis = Redis()
    r = await redis.get_redis_pool(('127.0.0.1', 6379), db=0, encoding='utf-8')

    value = await r.set(key, value, expire=expire)
    await redis.close()
    return value


templates = Jinja2Templates(directory='templates')


@app.get('/')
async def index_page(request: Request):
    template_name = 'index.html'
    return templates.TemplateResponse(template_name, {'request': request})



@app.post('/g/')
async def generate_handler(item: Item):
    code = get_short_url_code(item.url)

    await set_value(code, item.url)

    return {'code': code}


@app.get('/a/{short_code}')
async def redirect_handler(short_code: str):
    url = await get_value(short_code)
    if not url:
        url = 'https://cattalk.in/'

    return RedirectResponse(url)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8001)
