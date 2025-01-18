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

from re import match as re_match

# no longer used-links not found in plot these days
def cleanPlot(plot):
	if not plot: return
	try:
		index = plot.rfind('See full summary')
		if index == -1: index = plot.rfind("It's publicly available on")
		if index >= 0: plot = plot[:index]
		plot = plot.strip()
		if re_match(r'[a-zA-Z\d]$', plot): plot += ' ...'
		return plot
	except:
		from resources.lib.modules import log_utils
		log_utils.error()