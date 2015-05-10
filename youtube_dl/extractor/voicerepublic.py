# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

from ..compat import (
    compat_urllib_request,
)


class VoiceRepublicIE(InfoExtractor):
    _VALID_URL = r'https?://voicerepublic\.com/talks/(?P<id>[0-9a-z-]+)'
    _TEST = {
        'url': 'https://voicerepublic.com/talks/watching-the-watchers-building-a-sousveillance-state',
        'md5': '0554a24d1657915aa8e8f84e15dc9353',
        'info_dict': {
            'id': '2296',
            'ext': 'm4a',
            'title': 'Watching the Watchers: Building a Sousveillance State',
            'thumbnail': 'https://voicerepublic.com/system/flyer/2296.png',
            'description': 'md5:715ba964958afa2398df615809cfecb1',
            'creator': 'M. C. McGrath',
        }
    }

    def _real_extract(self, url):
        display_id = self._match_id(url)
        req = compat_urllib_request.Request(url)
        # Older versions of Firefox get redirected to an "upgrade browser" page
        req.add_header('User-Agent', 'youtube-dl')
        webpage = self._download_webpage(req, display_id)
        thumbnail = self._og_search_thumbnail(webpage)
        video_id = self._search_regex(r'/(\d+)\.png', thumbnail, 'id')

        if '<div class=\'vr-player jp-jplayer\'' in webpage:
            formats = [{
                'url': 'https://voicerepublic.com/vrmedia/{}-clean.{}'.format(video_id, ext),
                'ext': ext,
                'format_id': ext,
                'vcodec': 'none',
            } for ext in ['m4a', 'mp3', 'ogg']]
            self._sort_formats(formats)
        else:
            # Audio is still queued for processing
            formats = []

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'formats': formats,
            'url': self._og_search_url(webpage),
            'thumbnail': thumbnail,
            'description': self._og_search_description(webpage),
            'creator': self._html_search_meta('author', webpage),
        }
