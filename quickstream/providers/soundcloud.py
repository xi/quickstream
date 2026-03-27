import json

from ..base import provider


def get_trackinfo(soup):
    extra = {}
    for el in soup.select('script'):
        if el.text.startswith('window.__sc_hydration'):
            hydration = json.loads(el.text[24:-1])
            for item in hydration:
                if item['hydratable'] == 'apiClient':
                    extra['_client_id'] = item['data']['id']
                if item['hydratable'] == 'sound':
                    return {**item['data'], **extra}


async def get_streams(client, trackinfo):
    for item in trackinfo['media']['transcodings']:
        if item['snipped'] or '/preview/' in item['url']:
            continue
        if item['format']['protocol'] not in ['hls', 'progressive']:
            continue

        streaminfo = await client.fetch_json(item['url'], params={
            'client_id': trackinfo['_client_id'],
            'track_authorization': trackinfo['track_authorization'],
        })
        return streaminfo['url']


@provider(r'https?://soundcloud.com/([^/]+)/([^/]+)', tests={
    'http://soundcloud.com/ethmusic/lostin-powers-she-so-heavy': {
        'id': 62986583,
        'url': 'https://soundcloud.com/ethmusic/lostin-powers-she-so-heavy',
        'title': 'Lostin Powers - She so Heavy (SneakPreview) Adrian Ackers Blueprint 1',  # noqa
        'duration': 143.216,
    },
})
async def soundcloud_track(client, url, uploader, id):
    soup = await client.fetch_html(url)
    trackinfo = get_trackinfo(soup)
    return {
        'id': trackinfo['id'],
        'url': trackinfo['permalink_url'],
        'title': trackinfo['title'],
        'duration': trackinfo['duration'] / 1000,
        'stream': await get_streams(client, trackinfo),
    }
