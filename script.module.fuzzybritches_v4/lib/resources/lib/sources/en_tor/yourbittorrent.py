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
try: from urllib import urlencode, unquote_plus, quote_plus
except ImportError: from urllib.parse import urlencode, unquote_plus, quote_plus

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import workers
from resources.lib.modules import utils


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = ['yourbittorrent2.com']
        self.base_link = 'https://yourbittorrent.com'
        self.search_link = '/?v=&c=&q=%s'


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
        self.sources = []
        try:
            if url is None:
                return self.sources

            if debrid.status() is False:
                return self.sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            self.year = data['year']

            query = '%s %s' % (self.title, self.hdlr)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url)
            # log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

            try:
                r = client.request(url)
                links = re.findall('<a href="(/torrent/.+?)"', r, re.DOTALL)

                threads = []
                for link in links:
                    threads.append(workers.Thread(self.get_sources, link))
                [i.start() for i in threads]
                [i.join() for i in threads]
                return self.sources
            except:
                return self.sources

        except:
            return self.sources


    def get_sources(self, link):
        try:
            url = '%s%s' % (self.base_link, link)
            result = client.request(url)

            info_hash = re.findall('<kbd>(.+?)<', result, re.DOTALL)[0]
            url = '%s%s' % ('magnet:?xt=urn:btih:', info_hash)
            name = re.findall('<h3 class="card-title">(.+?)<', result, re.DOTALL)[0]
            url = '%s%s%s' % (url, '&dn=', str(name))

            size = re.findall('<div class="col-3">File size:</div><div class="col">(.+?)<', result, re.DOTALL)[0]

            if url in str(self.sources):
                return

            if any(x in url.lower() for x in ['french', 'italian', 'spanish', 'truefrench', 'dublado', 'dubbed']):
                return

            t = name.split(self.hdlr)[0].replace(self.year, '').replace('(', '').replace(')', '').replace('&', 'and').replace('+', ' ')

            if cleantitle.get(t) != cleantitle.get(self.title):
                return

            if self.hdlr not in name:
                return

            quality, info = source_utils.get_release_quality(name, url)

            try:
                size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', size)[0]
                div = 1 if size.endswith('GB') else 1024
                size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                size = '%.2f GB' % size
                info.insert(0, size)
            except:
                size = '0'
                pass

            info = ' | '.join(info)

            self.sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                                'info': info, 'direct': False, 'debridonly': True})

        except:
            pass

    def resolve(self, url):
        return url