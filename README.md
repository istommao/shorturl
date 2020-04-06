# shorturl
short url

- view https://s.cattalk.in/

## 相关推荐

- [小码短链接](https://xiaomark.com/)
- [毛驴短链](https://www.admqr.com/)
- [百度短网址](https://dwz.cn/)
- http://sina-t.cn/
- https://www.985.so/
- https://tool.chinaz.com/tools/dwz.aspx
- http://aliurl.cn/

---

- [文章/高性能短链设计](https://juejin.im/post/5e6ddef66fb9a07cb427ee13)
- https://www.cnblogs.com/rjzheng/p/11827426.html
- https://time.geekbang.org/column/article/80850

## shorturl 实现

- python3
- [xxhash_cffi / Extremely fast non-cryptographic hash algorithm](https://github.com/ifduyue/python-xxhash-cffi)
    C语言版本 https://github.com/Cyan4973/xxHash
- redis

```python
import xxhash_cffi

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(dec):
    return ALPHABET[dec] if dec < 62 else base62_encode(dec // 62) + ALPHABET[dec % 62]


def get_short_url_code(url):
    hash_num = xxhash_cffi.xxh32_intdigest(url)
    code = base62_encode(hash_num)

    return code

url = 'https://example.domain.com/router/'
code = get_short_url_code(url)

# 将 code 放入 redis缓存
# 用户 路由请求后 查询缓存 Redirect 重定向
```
