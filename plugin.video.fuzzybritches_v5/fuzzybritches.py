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

"""
	FuzzyBritches Add-on
"""

import sys
from resources.lib.modules import router
from xbmc import getInfoLabel
if __name__ == '__main__':
	router.router(sys.argv[2])
	if 'fuzzybritches' not in getInfoLabel('Container.PluginName'): sys.exit(1)