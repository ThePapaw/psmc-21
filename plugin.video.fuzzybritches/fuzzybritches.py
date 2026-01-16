# -*- coding: utf-8 -*-
"""
	FuzzyBritches Add-on
"""

import sys
from resources.lib.modules import router
from xbmc import getInfoLabel
if __name__ == '__main__':
	router.router(sys.argv[2])
	if 'fuzzybritches' not in getInfoLabel('Container.PluginName'): sys.exit(1) #TikiPeter RLI-Fix Test