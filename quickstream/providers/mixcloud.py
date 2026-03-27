import base64
import itertools
import json

from ..base import provider

DECRYPTION_KEY = b'IFYOUWANTTHEARTISTSTOGETPAIDDONOTDOWNLOADFROMMIXCLOUD'
QUERY = """
query cloudcastQuery($lookup: CloudcastLookup!) {
    cloudcast: cloudcastLookup(lookup: $lookup) {
        name
        audioLength
        streamInfo { url }
    }
}
"""


def decrypt(text):
    raw = base64.b64decode(text)
    pairs = zip(raw, itertools.cycle(DECRYPTION_KEY), strict=False)
    result = bytes([x ^ y for x, y in pairs])
    return result.decode('utf-8')


@provider(
    r'https?://www.mixcloud\.com/([^/]+)/(?!stream|uploads|favorites|listens|playlists)([^/]+)/',  # noqa
    tests={
        'http://www.mixcloud.com/dholbach/cryptkeeper/': {
            'id': 'dholbach_cryptkeeper',
            'title': 'Cryptkeeper',
            'duration': 3723,
        },
    },
)
async def mixcloud_track(client, url, username, slug):
    data = await client.graphql('https://app.mixcloud.com/graphql', QUERY, lookup={
        'username': username,
        'slug': slug,
    })
    trackinfo = data['data']['cloudcast']

    return {
        'id': f'{username}_{slug}',
        'title': trackinfo['name'],
        'duration': trackinfo['audioLength'],
        'stream': decrypt(trackinfo['streamInfo']['url']),
    }
