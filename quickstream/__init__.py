import argparse
import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup

from .base import registry
from .providers import bandcamp  # noqa
from .providers import mixcloud  # noqa
from .providers import soundcloud  # noqa

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--verbose', action='store_true')


class Client:
    def __init__(self, session):
        self.session = session

    async def fetch(self, url, **kwargs):
        async with await self.session.get(url, **kwargs) as r:
            return await r.read()

    async def fetch_html(self, url, **kwargs):
        html = await self.fetch(url, **kwargs)
        return BeautifulSoup(html, 'html.parser')

    async def fetch_json(self, url, **kwargs):
        async with await self.session.get(url, **kwargs) as r:
            return await r.json()

    async def graphql(self, url, query, **kwargs):
        async with await self.session.post(url, json={
            'query': query,
            'variables': kwargs,
        }) as r:
            return await r.json()


async def extract(url):
    for pattern, fn in registry:
        m = pattern.match(url)
        if not m:
            continue
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            return await fn(Client(session), url, *m.groups())


def main():
    args = parser.parse_args()
    data = asyncio.run(extract(args.url))
    if args.verbose:
        print(json.dumps(data, indent=2))
    else:
        print(data['stream'])
