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
import xbmc
try: #Py2
	from urlparse import parse_qsl
	from urllib import quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qsl, quote_plus

if __name__ == '__main__':
	item = sys.listitem
	path = item.getPath()
	plugin = 'plugin://plugin.video.fuzzybritches_v5/'
	args = path.split(plugin, 1)
	params = dict(parse_qsl(args[1].replace('?', '')))

	year = params.get('year')
	name = params.get('title') + ' (%s)' % year

	if 'tvshowtitle' in params:
		season = params.get('season', '')
		episode = params.get('episode', '')
		name = params.get('tvshowtitle') + ' S%02dE%02d' % (int(season), int(episode))
	sysname = quote_plus(name)

	fuzzybritches_path = 'RunPlugin(%s?action=cache_clearBookmark&name=%s&year=%s&opensettings=false)' % (plugin, sysname, year)
	xbmc.executebuiltin(fuzzybritches_path)

	path = path.split('&meta=')[0]
	kodi_path = 'RunPlugin(%s?action=cache_clearKodiBookmark&url=%s)' % (plugin, quote_plus(path))
	xbmc.executebuiltin(kodi_path)
	xbmc.executebuiltin('UpdateLibrary(video,special://skin/foo)')