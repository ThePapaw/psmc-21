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
except ImportError: #Py3
	from urllib.parse import parse_qsl, quote_plus

if __name__ == '__main__':
	item = sys.listitem
	info = item.getVideoInfoTag()
	type = info.getMediaType()
	name = info.getTitle()
	tvshowtitle = info.getTVShowTitle()
	if tvshowtitle:
		name = tvshowtitle
	# season = info.getSeason() # may utilize for season specific trailer search
	year = info.getYear()

	#trailer.Trailer().play_select(type, name, year, windowedtrailer=0)
	xbmc.executebuiltin('RunPlugin(plugin://plugin.video.fuzzybritches_v5/?action=play_Trailer_Select&type=%s&name=%s&year=%s&windowedtrailer=0,return)' % (type, name, year))