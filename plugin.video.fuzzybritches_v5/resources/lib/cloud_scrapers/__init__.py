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

import os
from pkgutil import walk_packages
from resources.lib.modules.control import setting as getSetting
from resources.lib.modules import log_utils
debug_enabled = getSetting('debug.enabled') == 'true'

def cloudSources():
	try:
		sourceDict = []
		sourceFolderLocation = os.path.dirname(__file__)
		for loader, module_name, is_pkg in walk_packages([sourceFolderLocation]):
			if is_pkg or 'cloud_utils' in module_name: continue
			if enabledCheck(module_name):
				try:
					module = loader.find_module(module_name).load_module(module_name)
					sourceDict.append((module_name, module.source))
				except Exception as e:
					if debug_enabled:
						from resources.lib.modules import log_utils
						log_utils.log('Error: Loading cloud scraper module: "%s": %s' % (module_name, e), level=log_utils.LOGWARNING)
		return sourceDict
	except:
		from resources.lib.modules import log_utils
		log_utils.error()
		return []

def enabledCheck(cloud_scraper):
	parent_dict = {'ad_cloud': 'alldebrid', 'pm_cloud': 'premiumize', 'rd_cloud': 'realdebrid'}
	try:
		parent_setting = parent_dict[cloud_scraper]
		from resources.lib.modules import log_utils
		log_utils.log('cloud scraper token check: %stoken' % (parent_setting), level=log_utils.LOGDEBUG)
		if not getSetting(parent_setting + 'token'): return False
		if getSetting(parent_setting + '.enable') == 'true' and getSetting(cloud_scraper + '.enabled') == 'true': return True
		else: return False
	except:
		from resources.lib.modules import log_utils
		log_utils.error()
		return False