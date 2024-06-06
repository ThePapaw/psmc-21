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
from resources.lib.modules import client
from resources.lib.modules import source_utils

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus
except ImportError: from urllib.parse import urlencode, quote_plus

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['soap2day.app']
        self.base_link = 'https://soap2day.app'
        self.post_link = '/engine/ajax/controller.php?mod=search'

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

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = data['title']
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            post = 'do=search&subaction=search&story=%s' % quote_plus(query)

            r = client.request(self.base_link, post=post)
            r = client.parseDOM(r, 'div', attrs={'class': 'thumbnail text-center'})
            for r in r:
                r = re.findall('<p><a href="(.+?)" title="(.+?)">.+?</a></p>', r, re.DOTALL)
                if data['title'] not in r[0][1]:
                    continue

            hostDict = hostprDict + hostDict

            for item in r:
                try:
                    data = client.request(item[0])
                    url = re.compile('src="(https://embed.mystream.+?)"').findall(data)
                    for url in url:
                        url = url.replace('https://embed.mystream.best/', 'https://embed.mystream.to/')
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,'debridonly': False})

                except:
                    pass

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
