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

from json import dumps as jsdumps, loads as jsloads
import sys
import xbmc
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

	year = params.get('year', '')
	imdb = params.get('imdb', '')
	tmdb = params.get('tmdb', '')
	tvdb = params.get('tvdb', '')
	season = params.get('season', '')
	episode = params.get('episode', '')
	tvshowtitle = params.get('tvshowtitle', '')
	systvshowtitle = quote_plus(tvshowtitle)
	meta = jsloads(params['meta'])
	sysmeta = quote_plus(jsdumps(meta))

# to browse by Progress
	xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.fuzzybritches_v5/?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&meta=%s&season=%s&episode=%s,return)' % (systvshowtitle, year, imdb, tmdb, tvdb, sysmeta, season, episode))

# # to browse full episode list
	# xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.fuzzybritches_v5/?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&meta=%s&season=%s,return)' % (systvshowtitle, year, imdb, tmdb, tvdb, sysmeta, season))