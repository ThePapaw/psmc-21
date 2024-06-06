# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v4
# Addon id: plugin.video.fuzzybritches_v4
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

from sys import argv

from resources.lib.modules import fuzzybritchesv4
from urllib.parse import parse_qsl

try:
	params = dict(parse_qsl(argv[2].replace('?', '')))
except:
	params = {}

fuzzybritchesv4.router(params)