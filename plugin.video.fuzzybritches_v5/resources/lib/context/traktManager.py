# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v5
# Addon id: plugin.video.fuzzybritches_v5
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches v5 Add-on
'''

import sys
from xbmc import getInfoLabel, executebuiltin
try: #Py2
	from urlparse import parse_qsl
	from urllib import quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qsl, quote_plus

if __name__ == '__main__':
	item = sys.listitem
	# message = item.getLabel()
	path = item.getPath()

	plugin = 'plugin://plugin.video.fuzzybritches_v5/'
	args = path.split(plugin, 1)
	params = dict(parse_qsl(args[1].replace('?', '')))
	name = params['tvshowtitle'] if 'tvshowtitle' in params else params['title']
	sysname = quote_plus(name)

	imdb = params.get('imdb', '')
	tvdb = params.get('tvdb', '')
	season = params.get('season', '')
	episode = params.get('episode', '')

	playcount = getInfoLabel('ListItem.Playcount')
	watched = (int(playcount) >= 1) if playcount else False

	path = 'RunPlugin(%s?action=tools_traktManager&name=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&watched=%s)' % (
				plugin, sysname, imdb, tvdb, season, episode, watched)
	executebuiltin(path)