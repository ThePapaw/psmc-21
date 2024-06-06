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

try: from urlparse import parse_qs, urljoin, urlparse
except ImportError: from urllib.parse import parse_qs, urljoin, urlparse
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus

from six import ensure_text

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['scene-rls.com', 'scene-rls.net']
        self.base_link = 'http://scene-rls.net'
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
                raise Exception()

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (title, int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (title, data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            try:
                url = self.search_link % quote_plus(query)
                url = urljoin(self.base_link, url)

                r = client.request(url)
                r = ensure_text(r, errors='replace')

                posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

                items = []

                for post in posts:
                    try:
                        u = client.parseDOM(post, "div", attrs={"class": "postContent"})
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', u[0])[0]
                        u = client.parseDOM(u, "h2")
                        u = client.parseDOM(u, 'a', ret='href')
                        u = [(i.strip('/').split('/')[-1], i, size) for i in u]
                        items += u
                    except:
                        pass
            except:
                pass

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) == cleantitle.get(title): continue

                    quality, info = source_utils.get_release_quality(name, item[1])

                    try:
                        dsize, isize = source_utils._size(item[2])
                    except:
                        dsize, isize = 0.0, ''
                    info.insert(0, isize)

                    info = ' | '.join(info)

                    url = item[1]
                    if any(x in url for x in ['.rar', '.zip', '.iso']):
                        raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = ensure_text(url)

                    host = re.findall('([\w]+[.][\w]+)$', urlparse(url.strip().lower()).netloc)[0]
                    if host not in hostDict:
                        raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = ensure_text(host)

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


