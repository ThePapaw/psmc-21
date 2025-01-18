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

from json import dumps as jsdumps
from resources.lib.modules.control import dialog, addonIcon, setting as getSetting
from resources.lib.windows.base import BaseDialog

class IconScrape(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 2086
		self.closed = False
		self.meta = kwargs.get('meta')
		self.highlight_color = getSetting('sources.highlight.color')
		self.icon = addonIcon()

	def run(self):
		self.doModal()
		self.clearProperties()

	def onInit(self):
		self.set_controls()

	def onAction(self, action):
		if action in self.closing_actions or action in self.selection_actions:
			self.doClose()

	def doClose(self):
		self.closed = True
		self.close()
		del self

	def iscanceled(self):
		return self.closed

	def set_controls(self):
		self.setProperty('fuzzybritches.highlight.color', self.highlight_color)
		self.setProperty('percent', str(0))

	def update(self, percent=0, content='', icon=None):
		try:
			self.getControl(5000).setPercent(percent)
			self.setProperty('percent', str(percent))
		except: pass