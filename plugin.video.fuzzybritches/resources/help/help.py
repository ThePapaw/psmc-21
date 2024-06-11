# -*- coding: utf-8 -*-
"""
	FuzzyBritches Add-on
"""

from resources.lib.modules.control import addonPath, addonId, getFuzzyBritchesVersion, joinPath
from resources.lib.windows.textviewer import TextViewerXML


def get(file):
	fuzzybritches_path = addonPath(addonId())
	fuzzybritches_version = getFuzzyBritchesVersion()
	helpFile = joinPath(fuzzybritches_path, 'resources', 'help', file + '.txt')
	f = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = f.read()
	f.close()
	heading = '[B]FuzzyBritches -  v%s - %s[/B]' % (fuzzybritches_version, file)
	windows = TextViewerXML('textviewer.xml', fuzzybritches_path, heading=heading, text=text)
	windows.run()
	del windows