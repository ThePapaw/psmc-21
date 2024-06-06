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

from six import ensure_text

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode
except ImportError: from urllib.parse import urlencode

from resources.lib.modules import debrid, cleantitle, client, source_utils, log_utils, cfscrape

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bt4g.org']
        self.base_link = 'https://bt4g.org'
        self.search_link = '/movie/search/%s/byseeders/1'

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
            if url is None: return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        scraper = cfscrape.create_scraper()
        try:
            if debrid.status() is False:
                return sources

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))\
                                       if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub(u'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query).lower()

            url = urljoin(self.base_link, self.search_link % query)

            #r = client.request(url)
            #r = requests.get(url).content
            r = scraper.get(url).content
            r = ensure_text(r, errors='replace').replace('&nbsp;', ' ')
            r = client.parseDOM(r, 'div', attrs={'class': 'col s12'})
            posts = client.parseDOM(r, 'div')[1:]
            posts = [i for i in posts if 'magnet/' in i]
            for post in posts:

                links = client.parseDOM(post, 'a', ret='href')[0]
                url = 'magnet:?xt=urn:btih:' + links.lstrip('magnet/')
                try:
                    name = client.parseDOM(post, 'a', ret='title')[0]
                    if not query in cleantitle.get_title(name): continue
                except:
                    name = ''

                quality, info = source_utils.get_release_quality(name, name)
                try:
                    size = re.findall(r'<b class="cpill .+?-pill">(.+?)</b>', post)[0]
                    dsize, isize = source_utils._size(size)
                except:
                    dsize, isize = 0.0, ''

                info.insert(0, isize)

                info = ' | '.join(info)

                sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                'direct': False, 'debridonly': True, 'size': dsize, 'name': name})

            return sources
        except:
            log_utils.log('bt4g3 - Exception', 1)
            return sources

    def resolve(self, url):
        return url
