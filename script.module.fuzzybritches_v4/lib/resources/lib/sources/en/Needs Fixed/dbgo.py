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

import re,base64
from resources.lib.modules import client, source_utils

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['dbgo.fun']
        self.base_link = 'https://dbgo.fun'
        self.search_link = '/video.php?id=%s'
        self.headers = {'Referer': 'https://cdn.dbgo.fun'}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = self.search_link % quote_plus(data['imdb'])
            url = urljoin(self.base_link, url)
            try:
                url = client.request(url, headers=self.headers)
                print('DBGO_URL', url)
                url = re.findall('file:"#2(.*?)"', url)[0]
                url = re.sub(r'\/\/\w{8}',"",url)
                url = base64.b64decode(url).decode('utf-8') + '|Referer=https://cdn.dbgo.fun/'
                quality = source_utils.check_direct_url(url)
                sources.append({'source': 'CDN', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                pass

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
