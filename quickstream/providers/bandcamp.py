import json

from ..base import provider


def get_stream(trackinfo):
    for _fmt, url in trackinfo['file'].items():
        return url


@provider(r'https?://([^/]+)\.bandcamp\.com/track/([^/?#&]+)', tests={
    'http://benprunty.bandcamp.com/track/lanius-battle': {
        'id': 2650410135,
        'url': 'https://benprunty.bandcamp.com/track/lanius-battle',
        'title': 'Lanius (Battle)',
        'duration': 260.877,
    },
})
async def bandcamp_track(client, url, uploader, id):
    soup = await client.fetch_html(url)
    el = soup.select_one('[data-tralbum]')
    tralbum = json.loads(el['data-tralbum'])
    trackinfo = tralbum['trackinfo'][0]
    return {
        'id': trackinfo['id'],
        'url': tralbum['url'],
        'title': trackinfo['title'],
        'duration': trackinfo['duration'],
        'stream': get_stream(trackinfo),
    }
