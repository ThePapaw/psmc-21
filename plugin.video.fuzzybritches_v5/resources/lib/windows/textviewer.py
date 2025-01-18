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

from resources.lib.windows.base import BaseDialog
from resources.lib.modules.control import isDarkColor, setting as getSetting, log


class TextViewerXML(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 2060
		self.heading = kwargs.get('heading','FuzzyBritches')
		self.text = kwargs.get('text')
		self.lightordark = getSetting('dialogs.lightordarkmode')
		self.buttonColor = getSetting('dialogs.button.color')
		self.customBackgroundColor = getSetting('dialogs.customcolor')
		log('customBackgroundColor: %s' % self.customBackgroundColor,1)
		self.dark_text_background = isDarkColor(self.customBackgroundColor)
		self.useCustomTitleColor = getSetting('dialogs.usecolortitle') == 'true'
		self.customTitleColor = getSetting('dialogs.titlebar.color')

	def onInit(self):
		self.set_properties()
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		self.clearProperties()

	def onAction(self, action):
		if action in self.closing_actions or action in self.selection_actions:
			self.close()

	def set_properties(self):
		self.setProperty('fuzzybritches.text', self.text)
		self.setProperty('fuzzybritches.heading', self.heading)
		self.setProperty('fuzzybritches.buttonColor', self.buttonColor)
		if self.useCustomTitleColor:
			#need to use a custom titlebar color
			self.setProperty('fuzzybritches.titleBarColor', self.customTitleColor)
			log('customTitleColor: %s' % self.customTitleColor,1)
			if isDarkColor(self.customTitleColor):
				self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
			else:
				self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
			self.setProperty('fuzzybritches.headertextcolor', self.customTitleColor)
		log('button color: %s '% self.buttonColor,1)
		if isDarkColor(self.buttonColor):
			self.setProperty('fuzzybritches.buttonTextColor', 'FFF5F5F5')
		else:
			self.setProperty('fuzzybritches.buttonTextColor', 'FF302F2F')
		if self.lightordark == '0':
			self.setProperty('fuzzybritches.backgroundColor', 'FF302F2F') #setting dark grey for dark mode
			self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
			self.setProperty('fuzzybritches.buttonnofocus', 'FF302F2F')
			if not self.useCustomTitleColor:
				self.setProperty('fuzzybritches.headertextcolor', self.buttonColor)
				self.setProperty('fuzzybritches.titleBarColor', 'FF302F2F')
				self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
			self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
		elif self.lightordark == '1':
			self.setProperty('fuzzybritches.backgroundColor', 'FFF5F5F5') #setting dirty white for light mode. (the hell you call me)
			self.setProperty('fuzzybritches.textColor', 'FF302F2F')
			self.setProperty('fuzzybritches.buttonnofocus', 'FFF5F5F5')
			if not self.useCustomTitleColor:
				self.setProperty('fuzzybritches.headertextcolor', self.buttonColor)
				self.setProperty('fuzzybritches.titleBarColor', 'FFF5F5F5')
				self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
			self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
		elif self.lightordark == '2':
			#ohh now we need a custom color, aren't we just special.
			self.setProperty('fuzzybritches.backgroundColor', self.customBackgroundColor) #setting custom color because screw your light or dark mode.
			self.setProperty('fuzzybritches.buttonnofocus', self.customBackgroundColor) #set button same as custom background color when not selected
			if self.dark_text_background == 'dark':
				self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
				self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
				if not self.useCustomTitleColor:
					self.setProperty('fuzzybritches.headertextcolor', self.buttonColor)
					self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
					self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor) #setting titletext and background color if not using a custom value
			else:
				self.setProperty('fuzzybritches.textColor', 'FF302F2F')
				self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
				if not self.useCustomTitleColor:
					self.setProperty('fuzzybritches.headertextcolor', self.buttonColor)
					self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
					self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor)#setting titletext and background color if not using a custom value