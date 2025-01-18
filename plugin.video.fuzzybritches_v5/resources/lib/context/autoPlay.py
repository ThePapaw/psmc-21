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
try: #PY2
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

	title = params['title']
	systitle = quote_plus(title)
	year = params.get('year', '')

	if 'meta' in params:
		meta = jsloads(params['meta'])
		imdb = meta.get('imdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')
		tvshowtitle = meta.get('tvshowtitle', '').encode('utf-8', 'ignore')
		systvshowtitle = quote_plus(tvshowtitle)
		premiered = meta.get('premiered', '')
	else:
		imdb = params.get('imdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')
		tvshowtitle = params.get('tvshowtitle', '')
		systvshowtitle = quote_plus(tvshowtitle)
		premiered = params.get('premiered', '')

	sysmeta = quote_plus(jsdumps(meta))

	if 'tvshowtitle' in meta:
		url = '%s?action=play_Item&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s' % (
								plugin, systitle, year, imdb, tvdb, season, episode, systvshowtitle, premiered, sysmeta)
	else:
		url = '%s?action=play_Item&title=%s&year=%s&imdb=%s&meta=%s' % (plugin, systitle, year, imdb, sysmeta)
	sysurl = quote_plus(url)
	path = 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (plugin, sysurl, sysmeta)
	xbmc.executebuiltin(path)