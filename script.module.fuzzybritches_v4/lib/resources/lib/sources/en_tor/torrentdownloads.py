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

from resources.lib.modules import debrid
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import source_utils

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus, quote
except ImportError: from urllib.parse import urlencode, quote_plus, quote


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['torrentdownloads.me']
        self.base_link = 'https://www.torrentdownloads.me'
        self.search = 'https://www.torrentdownloads.me/rss.xml?new=1&type=search&cid={0}&search={1}'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except BaseException:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            if url is None:
                return self._sources

            if debrid.status() is False:
                raise Exception()

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = self.search.format('8', quote(query))
            else:
                url = self.search.format('4', quote(query))

            self.hostDict = hostDict + hostprDict
            headers = {'User-Agent': client.agent()}
            _html = client.request(url, headers=headers)
            threads = []
            for i in re.findall(r'<item>(.+?)</item>', _html, re.DOTALL):
                threads.append(workers.Thread(self._get_items, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self._sources
        except BaseException:
            return self._sources

    def _get_items(self, r):
        try:
            size = re.search(r'<size>([\d]+)</size>', r).groups()[0]
            seeders = re.search(r'<seeders>([\d]+)</seeders>', r).groups()[0]
            _hash = re.search(r'<info_hash>([a-zA-Z0-9]+)</info_hash>', r).groups()[0]
            name = re.search(r'<title>(.+?)</title>', r).groups()[0]
            url = 'magnet:?xt=urn:btih:%s&dn=%s' % (_hash.upper(), quote_plus(name))
            t = name.split(self.hdlr)[0]

            try:
                y = re.findall(r'[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
            except BaseException:
                y = re.findall(r'[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()

            try:
                div = 1000 ** 3
                size = float(size) / div
                size = '%.2f GB' % size
            except BaseException:
                size = '0'

            quality, info = source_utils.get_release_quality(name, name)
            info.append(size)
            info = ' | '.join(info)

            if not seeders == '0':
                if cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title):
                    if y == self.hdlr:
                        self._sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})

        except BaseException:
            pass

    def resolve(self, url):
        return url
