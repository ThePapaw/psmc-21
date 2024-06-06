# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v4 Module
# Addon id: script.module.fuzzybritches_v4
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import re

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus

from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['max-rls.com']
        self.base_link = 'http://max-rls.com'
        self.search_link = '/?s=%s&submit=Find'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            if debrid.status() is False:
                return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('%3A+', '+')

            r = client.request(url)
            if r is None and 'tvshowtitle' in data:
                season = re.search('S(.*?)E', hdlr)
                season = season.group(1)
                url = title

                r = client.request(url)

            for loopCount in list(range(0, 2)):
                if loopCount == 1 or (r is None and 'tvshowtitle' in data):

                    r = client.request(url)

                posts = client.parseDOM(r, "h2", attrs={"class": "postTitle"})
                hostDict = hostprDict + hostDict
                items = []
                for post in posts:
                    try:
                        u = client.parseDOM(post, 'a', ret='href')
                        for i in u:
                            name = str(i)
                            items.append(name)
                    except:
                        pass

                if len(items) > 0:
                    break

            for item in items:
                try:
                    i = str(item)
                    r = client.request(i)
                    u = client.parseDOM(r, "div", attrs={"class": "postContent"})
                    for t in u:
                        r = client.parseDOM(t, 'a', ret='href')
                        for url in r:
                            quality, info = source_utils.get_release_quality(url)
                            if 'SD' in quality:
                                continue
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
