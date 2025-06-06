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
Included with the Fuzzy Britches v4 Add-on
'''

import re

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus, unquote
except ImportError: from urllib.parse import urlencode, quote_plus, unquote

from resources.lib.modules import cleantitle, debrid, source_utils
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['isohunt2.net']
        self.base_link = 'https://isohunt.nz'
        self.search_link = '/torrent/?ihq=%s&fiht=2&age=0&Torrent_sort=seeders'

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
        sources = []
        try:
            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('++', '+')

            try:
                r = client.request(url)
                posts = client.parseDOM(r, 'tbody')[0]
                posts = client.parseDOM(posts, 'tr')
                for post in posts:
                    links = re.compile('<a href="(/torrent_details/.+?)">\n<span>(.+?)</span>').findall(post)
                    for link, data in links:
                        if hdlr not in data:
                            continue
                        link = urljoin(self.base_link, link)
                        if any(x in link for x in ['FRENCH', 'Ita', 'ITA', 'italian', 'Tamil', 'TRUEFRENCH', '-lat-', 'Dublado', 'Dub', 'Rus', 'Hindi']):
                                continue
                        link = client.request(link)
                        getsize = re.findall('Size&nbsp;(.+?)&nbsp', link, re.DOTALL)[0]
                        try:
                            size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', getsize)[0]
                            div = 1 if size.endswith('GB') else 1024
                            size = float(re.sub(r'[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                            size = '%.2f GB' % size
                        except BaseException:
                            size = '0'
                        link = re.findall('<a href="(https:.+?)"', link, re.DOTALL)
                        for url in link:
                            try: url = unquote(url).decode('utf8')
                            except: pass
                            url = url.split('url=')[1].split('&tr=')[0].replace('%28', '(').replace('%29',')')
                            quality, info = source_utils.get_release_quality(data)
                            info.append(size)
                            info = ' | '.join(info)
                            sources.append(
                                {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                 'direct': False, 'debridonly': True})
            except:
                return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
