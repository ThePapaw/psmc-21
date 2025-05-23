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

from xbmc import executebuiltin
from xbmcgui import WindowXMLDialog, ListItem, ControlProgress


class BaseDialog(WindowXMLDialog):
	def __init__(self, *args):
		WindowXMLDialog.__init__(self, args)
		self.closing_actions = [9, 10, 13, 92, 511]
		self.selection_actions = [7, 100]
		#self.ok_actions = [107,]
		self.context_actions = [101, 117]
		self.info_actions = [11,]
		# self.updn_actions = [5, 6]

	def make_listitem(self):
		return ListItem()

	def execute_code(self, command):
		return executebuiltin(command)

	def get_position(self, window_id):
		return self.getControl(window_id).getSelectedPosition()

	def getControlProgress(self, control_id):
		control = self.getControl(control_id)
		if not isinstance(control, ControlProgress):
			raise AttributeError("Control with Id {} should be of type ControlProgress".format(control_id))
		return control