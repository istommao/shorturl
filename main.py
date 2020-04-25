# coding: utf-8

from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import aioredis
import xxhash_cffi

app = FastAPI()


REDIS_CONFIG = ('127.0.0.1', 6379)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(dec):
    return ALPHABET[dec] if dec < 62 else base62_encode(dec // 62) + ALPHABET[dec % 62]


def get_short_url_code(url):
    hash_num = xxhash_cffi.xxh32_intdigest(url)
    code = base62_encode(hash_num)

    return code


class Item(BaseModel):
    url: str


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

from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
