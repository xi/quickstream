# quickstream

Find stream URIs for common streaming services.

This project is similar in spirit to [yt-dlp](https://github.com/yt-dlp/yt-dlp), with a few major differences:

-   focus on audio rather than video
-   focus on streaming rather than downloading
-   focus on finding a usable URI quickly rather than finding the best one
-   modern, clean code
-   much smaller set of supported sites (due to a much smaller community)

## usage

```python
>>> import quickstream
>>> await quickstream.extract('http://youtube-dl.bandcamp.com/track/youtube-dl-test-song')
{
    'id': 1812978515,
    'url': 'https://youtube-dl.bandcamp.com/track/youtube-dl-test-song',
    'title': 'youtube-dl  "\'/\\ä↭ - youtube-dl test song "\'/\\ä↭',
    'duration': 9.8485,
    'stream': 'https://t4.bcbits.com/stream/de52650df97feb66af7cdb75ab0e20fa/mp3-128/1812978515?p=0&ts=1774681098&t=18489d2f73b58b6e5dbb97b30327531ae00776eb&token=1774681098_b56e7617d9e5f3c784567aa84a36ed7d077ccde8',
}
```
