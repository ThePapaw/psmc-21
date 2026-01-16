# -*- coding: utf-8 -*-

import xbmc

if __name__ == '__main__':
	plugin = 'plugin://plugin.video.fuzzybritches/'
	path = 'RunPlugin(%s?action=tools_contextFuzzyBritchesSettings&opensettings=false)' % plugin
	xbmc.executebuiltin(path)
	# xbmc.executebuiltin('RunPlugin(%s?action=widgetRefresh)' % plugin) #now part of "tools_contextFuzzyBritchesSettings" action