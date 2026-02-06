# -*- coding: utf-8 -*-
"""
	FuzzyBritches Add-on
"""

from resources.lib.modules.control import joinPath, artPath, setting as getSetting
from resources.lib.windows.base import BaseDialog


class TraktLikedListManagerXML(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 2050
		self.results = kwargs.get('results')
		self.total_results = str(len(self.results))
		self.highlight_color = getSetting('highlight.color')
		self.selected_items = []
		self.make_items()
		self.set_properties()

	def onInit(self):
		win = self.getControl(self.window_id)
		win.addItems(self.item_list)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		self.clearProperties()
		return self.selected_items

	# def onClick(self, controlID):
		# from resources.lib.modules import log_utils
		# log_utils.log('controlID=%s' % controlID)

	def onAction(self, action):
		try:
			if action in self.selection_actions:
				focus_id = self.getFocusId()
				if focus_id == 2050: # listItems
					position = self.get_position(self.window_id)
					chosen_listitem = self.item_list[position]
					trakt_id = chosen_listitem.getProperty('fuzzybritches.trakt_id')
					if chosen_listitem.getProperty('fuzzybritches.isSelected') == 'true':
						chosen_listitem.setProperty('fuzzybritches.isSelected', '')
						if trakt_id in str(self.selected_items):
							pos = next((index for (index, d) in enumerate(self.selected_items) if d["trakt_id"] == trakt_id), None)
							self.selected_items.pop(pos)
					else:
						chosen_listitem.setProperty('fuzzybritches.isSelected', 'true')
						list_owner = chosen_listitem.getProperty('fuzzybritches.list_owner')
						list_name = chosen_listitem.getProperty('fuzzybritches.list_name')
						self.selected_items.append({'list_owner': list_owner, 'list_name': list_name, 'trakt_id': trakt_id})
				elif focus_id == 2051: # OK Button
					self.close()
				elif focus_id == 2052: # Cancel Button
					self.selected_items = None
					self.close()
				elif focus_id == 2053: # Select All Button
					for item in self.item_list:
						item.setProperty('fuzzybritches.isSelected', 'true')
						self.selected_items.append({'list_owner': item.getProperty('fuzzybritches.list_owner'), 'list_name': item.getProperty('fuzzybritches.list_name'), 'trakt_id': item.getProperty('fuzzybritches.trakt_id')})
			elif action in self.closing_actions:
				self.selected_items = None
				self.close()
		except:
			from resources.lib.modules import log_utils
			log_utils.error()
			self.close()

	def make_items(self):
		def builder():
			for count, item in enumerate(self.results, 1):
				try:
					listitem = self.make_listitem()
					listitem.setProperty('fuzzybritches.list_owner', item.get('list_owner'))
					listitem.setProperty('fuzzybritches.list_name', str(item.get('list_name')))
					listitem.setProperty('fuzzybritches.trakt_id', str(item.get('trakt_id')))
					listitem.setProperty('fuzzybritches.item_count', str(item.get('item_count')))
					listitem.setProperty('fuzzybritches.likes', str(item.get('likes')))
					listitem.setProperty('fuzzybritches.isSelected', '')
					listitem.setProperty('fuzzybritches.count', '%02d.)' % count)
					yield listitem
				except:
					from resources.lib.modules import log_utils
					log_utils.error()
		try:
			self.item_list = list(builder())
			self.total_results = str(len(self.item_list))
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def set_properties(self):
		try:
			self.setProperty('fuzzybritches.total_results', self.total_results)
			self.setProperty('fuzzybritches.highlight.color', self.highlight_color)
			self.setProperty('fuzzybritches.trakt_icon', joinPath(artPath(), 'trakt.png'))
		except:
			from resources.lib.modules import log_utils
			log_utils.error()