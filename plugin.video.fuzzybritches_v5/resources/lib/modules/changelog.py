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

from resources.lib.modules.control import addonPath, addonVersion, joinPath, existsPath
from resources.lib.windows.textviewer import TextViewerXML


def get(name):
	nameDict = {'FuzzyBritches': 'plugin.video.fuzzybritches_v5'}
	addon_path = addonPath(nameDict[name])
	addon_version = addonVersion(nameDict[name])
	changelog_file = joinPath(addon_path, 'changelog.txt')
	if not existsPath(changelog_file):
		from resources.lib.modules.control import notification
		return notification(message='ChangeLog File not found.')
	f = open(changelog_file, 'r', encoding='utf-8', errors='ignore')
	text = f.read()
	f.close()
	heading = '[B]%s -  v%s - ChangeLog[/B]' % (name, addon_version)
	windows = TextViewerXML('textviewer.xml', addonPath('plugin.video.fuzzybritches_v5'), heading=heading, text=text)
	windows.run()
	del windows