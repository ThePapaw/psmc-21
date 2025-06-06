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
from urllib.parse import quote_plus
from resources.lib.modules.control import joinPath, transPath, dialog, notification, addonFanart, setting as getSetting, getProviderColors
from resources.lib.modules import tools
from resources.lib.windows.base import BaseDialog


class SourceResultsXML(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 2000
		self.results = kwargs.get('results')
		self.uncached = kwargs.get('uncached')
		self.total_results = str(len(self.results))
		self.meta = kwargs.get('meta')
		self.defaultbg = addonFanart()
		self.dnlds_enabled = True if getSetting('downloads') == 'true' and (getSetting('movie.download.path') != '' or getSetting('tv.download.path') != '') else False
		self.colors = getProviderColors()
		self.useProviderColors = True if self.colors['useproviders'] == True else False
		self.sourceHighlightColor = self.colors['defaultcolor']
		self.realdebridHighlightColor = self.colors['realdebrid']
		self.alldebridHighlightColor = self.colors['alldebrid']
		self.premiumizeHighlightColor = self.colors['premiumize']
		self.easynewsHighlightColor = self.colors['easynews']
		self.plexHighlightColor = self.colors['plexshare']
		self.gdriveHighlightColor = self.colors['gdrive']
		self.torboxHighlightColor = self.colors['torbox']
		self.easyDebridHighlightColor = self.colors['easydebrid']
		self.offcloudHighlightColor = self.colors['offcloud']
		#self.furkHighlightColor = self.colors['furk']
		self.filePursuitHighlightColor = self.colors['filepursuit']
		self.dialogColor = getSetting('scraper.dialog.color')
		self.highlight_color = getSetting('highlight.color')
		self.make_items()
		self.set_properties()

	def onInit(self):
		win = self.getControl(self.window_id)
		win.addItems(self.item_list)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		self.clearProperties()
		return self.selected

	def onAction(self, action):
		try:
			action_id = action.getId() # change to just "action" as the ID is already returned in that.
			if action_id in self.info_actions:
				chosen_source = self.item_list[self.get_position(self.window_id)]
				chosen_source = chosen_source.getProperty('fuzzybritches.source_dict')
				syssource = quote_plus(chosen_source)
				self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=sourceInfo&source=%s)' % syssource)
			if action_id in self.selection_actions:
				focus_id = self.getFocusId()
				if focus_id == 2001:
					position = self.get_position(self.window_id)
					self.load_uncachedTorrents()
					self.setFocusId(self.window_id)
					self.getControl(self.window_id).selectItem(position)
					self.selected = (None, '')
					return
				if focus_id == 2051:
					self.selected = (None, '')
					return self.close()
				chosen_source = self.item_list[self.get_position(self.window_id)]
				source = chosen_source.getProperty('fuzzybritches.source')
				if 'UNCACHED' in source:
					debrid = chosen_source.getProperty('fuzzybritches.debrid')
					source_dict = chosen_source.getProperty('fuzzybritches.source_dict')
					link_type = 'pack' if 'package' in source_dict else 'single'
					sysname = quote_plus(self.meta.get('title'))
					if 'tvshowtitle' in self.meta and 'season' in self.meta and 'episode' in self.meta:
						poster = self.meta.get('season_poster') or self.meta.get('poster')
						sysname += quote_plus(' S%02dE%02d' % (int(self.meta['season']), int(self.meta['episode'])))
					elif 'year' in self.meta: sysname += quote_plus(' (%s)' % self.meta['year'])
					try: new_sysname = quote_plus(chosen_source.getProperty('fuzzybritches.name'))
					except: new_sysname = sysname
					self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=cacheTorrent&caller=%s&type=%s&title=%s&items=%s&url=%s&source=%s&meta=%s)' %
											(debrid, link_type, sysname, quote_plus(jsdumps(self.results)), quote_plus(chosen_source.getProperty('fuzzybritches.url')), quote_plus(source_dict), quote_plus(jsdumps(self.meta))))
					self.selected = (None, '')
				else:
					self.selected = ('play_Item', chosen_source)
				return self.close()
			elif action_id in self.context_actions:
				from re import match as re_match
				chosen_source = self.item_list[self.get_position(self.window_id)]
				source_dict = chosen_source.getProperty('fuzzybritches.source_dict')
				cm_list = [('[B]Additional Link Info[/B]', 'sourceInfo')]
				if 'cached (pack)' in source_dict:
					cm_list += [('[B]Browse Debrid Pack[/B]', 'showDebridPack')]
				if 'unchecked (pack)' in source_dict:
					cm_list += [('[B]Browse Debrid Pack[/B]', 'showDebridPack')]
				source = chosen_source.getProperty('fuzzybritches.source')
				if not 'UNCACHED' in source and self.dnlds_enabled:
					cm_list += [('[B]Download[/B]', 'download')]
					cm_list += [('[B]Create Strm File[/B]', 'strmFile')]
				debrid = chosen_source.getProperty('fuzzybritches.debrid')
				if (re_match(r'^CACHED.*TORRENT', source) or 'unchecked' in source_dict) and debrid != 'EasyDebrid':
					cm_list += [('[B]Save to %s Cloud[/B]' % debrid, 'saveToCloud')]
				chosen_cm_item = dialog.contextmenu([i[0] for i in cm_list])
				if chosen_cm_item == -1: return
				cm_action = cm_list[chosen_cm_item][1]
				if cm_action == 'sourceInfo':
					self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=sourceInfo&source=%s)' % quote_plus(source_dict))
				elif cm_action == 'showDebridPack':
					debrid = chosen_source.getProperty('fuzzybritches.debrid')
					name = chosen_source.getProperty('fuzzybritches.name')
					hash = chosen_source.getProperty('fuzzybritches.hash')
					self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=showDebridPack&caller=%s&name=%s&url=%s&source=%s)' %
									(quote_plus(debrid), quote_plus(name), quote_plus(chosen_source.getProperty('fuzzybritches.url')), quote_plus(hash)))
					self.selected = (None, '')
				elif cm_action == 'download':
					sysname = quote_plus(self.meta.get('title'))
					poster = self.meta.get('poster', '')
					if 'tvshowtitle' in self.meta and 'season' in self.meta and 'episode' in self.meta:
						sysname = quote_plus(self.meta.get('tvshowtitle'))
						poster = self.meta.get('season_poster') or self.meta.get('poster')
						sysname += quote_plus(' S%02dE%02d' % (int(self.meta['season']), int(self.meta['episode'])))
					elif 'year' in self.meta: sysname += quote_plus(' (%s)' % self.meta['year'])
					try: new_sysname = quote_plus(chosen_source.getProperty('fuzzybritches.name'))
					except: new_sysname = sysname
					self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=download&name=%s&image=%s&source=%s&caller=sources&title=%s)' %
										(new_sysname, quote_plus(poster), quote_plus(source_dict), sysname))
					self.selected = (None, '')
				elif cm_action == 'strmFile':
					sysname = quote_plus(self.meta.get('title'))
					poster = self.meta.get('poster', '')
					if 'tvshowtitle' in self.meta and 'season' in self.meta and 'episode' in self.meta:
						sysname = quote_plus(self.meta.get('tvshowtitle'))
						poster = self.meta.get('season_poster') or self.meta.get('poster')
						sysname += quote_plus(' S%02dE%02d' % (int(self.meta['season']), int(self.meta['episode'])))
					elif 'year' in self.meta: sysname += quote_plus(' (%s)' % self.meta['year'])
					try: new_sysname = quote_plus(chosen_source.getProperty('fuzzybritches.name'))
					except: new_sysname = sysname
					self.execute_code('RunPlugin(plugin://plugin.video.fuzzybritches/?action=createStrm&name=%s&image=%s&source=%s&caller=sources&title=%s)' %
										(new_sysname, quote_plus(poster), quote_plus(source_dict), sysname))
					self.selected = (None, '')
				elif cm_action == 'saveToCloud':
					magnet = chosen_source.getProperty('fuzzybritches.url')
					if debrid == 'AllDebrid':
						from resources.lib.debrid import alldebrid
						transfer_function = alldebrid.AllDebrid
						debrid_icon = alldebrid.ad_icon
					elif debrid == 'Offcloud':
						from resources.lib.debrid import offcloud
						transfer_function = offcloud.Offcloud
						debrid_icon = offcloud.oc_icon
					elif debrid == 'Premiumize':
						from resources.lib.debrid import premiumize
						transfer_function = premiumize.Premiumize
						debrid_icon = premiumize.pm_icon
					elif debrid == 'Real-Debrid':
						from resources.lib.debrid import realdebrid
						transfer_function = realdebrid.RealDebrid
						debrid_icon = realdebrid.rd_icon
					elif debrid == 'TorBox':
						from resources.lib.debrid import torbox
						transfer_function = torbox.TorBox
						debrid_icon = torbox.tb_icon
					elif debrid == 'EasyDebrid':
						from resources.lib.debrid import easydebrid
						transfer_function = easydebrid.EasyDebrid
						debrid_icon = easydebrid.ed_icon
					result = transfer_function().create_transfer(magnet)
					if result: notification(message='Sending MAGNET to the %s cloud' % debrid, icon=debrid_icon)
			elif action in self.closing_actions:
				self.selected = (None, '')
				self.close()
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def get_quality_iconPath(self, quality):
		if str(quality) == '4K':
			quality = '4k'
		try:
			return joinPath(transPath('special://home/addons/plugin.video.fuzzybritches/resources/skins/Default/media/resolution'), '%s.png' % quality)
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def get_provider1_iconPath(self, provider):
		if str(quality) == '4K':
			quality = '4k'
		try:
			if provider == 'premiumize.me': provider = 'premiumize'
			return joinPath(transPath('special://home/addons/plugin.video.fuzzybritches/resources/skins/Default/media/resolution1'), '%s.png' % provider)
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def get_quality1_iconPath(self, quality):
		if str(quality) == '4K':
			quality = '4k'
		try:
			return joinPath(transPath('special://home/addons/plugin.video.fuzzybritches/resources/skins/Default/media/resolution1'), '%s.png' % quality)
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def debrid_abv(self, debrid):
		try:
			d_dict = {'AllDebrid': 'AD', 'EasyDebrid': 'ED','Premiumize.me': 'PM', 'Real-Debrid': 'RD', 'Torbox': 'TB', 'Offcloud': 'OC'}
			d = d_dict[debrid]
		except:
			d = ''
		return d

	def debrid_name(self, debrid):
		try:
			d_dict = {'AllDebrid': 'AllDebrid', 'EasyDebrid': 'EasyDebrid','Premiumize.me': 'Premiumize', 'Real-Debrid': 'Real-Debrid', 'TorBox': 'TorBox', 'Offcloud': 'Offcloud'}
			d = d_dict[debrid]
		except:
			d = ''
		return d

	def make_items(self):
		def builder():
			for count, item in enumerate(self.results, 1):
				try:
					listitem = self.make_listitem()
					quality = item.get('quality', 'SD')
					quality_icon = self.get_quality_iconPath(quality)
					quality1_icon = self.get_quality1_iconPath(quality)
					extra_info = item.get('info')
					#from resources.lib.modules import log_utils
					#log_utils.log('FuzzyBritches Sources Make Items: %s' % str(item.get('debrid')), log_utils.LOGINFO)
					if self.useProviderColors == True:
						if item.get('debrid') is not None and item.get('debrid') !='':
							if str(item.get('debrid')).lower() == 'real-debrid':
								providerHighlight = self.realdebridHighlightColor
							elif str(item.get('debrid')).lower() == 'alldebrid':
								providerHighlight = self.alldebridHighlightColor
							elif str(item.get('debrid')).lower()== 'premiumize.me':
								providerHighlight = self.premiumizeHighlightColor
							elif str(item.get('debrid')).lower()== 'torbox':
								providerHighlight = self.torboxHighlightColor
							elif str(item.get('debrid')).lower()== 'easydebrid':
								providerHighlight = self.easyDebridHighlightColor
							elif str(item.get('debrid')).lower()== 'offcloud':
								providerHighlight = self.offcloudHighlightColor
						else:
							if item.get('provider') == 'easynews':
								providerHighlight = self.easynewsHighlightColor
							elif str(item.get('provider')).lower() == 'plexshare':
								providerHighlight = self.plexHighlightColor
							elif str(item.get('provider')).lower() == 'gdrive':
								providerHighlight = self.gdriveHighlightColor
							elif str(item.get('provider')).lower() == 'filepursuit':
								providerHighlight = self.filePursuitHighlightColor
							else:
								providerHighlight = self.sourceHighlightColor
					else:
						providerHighlight = self.sourceHighlightColor
					size_label = str(round(item.get('size', ''), 2)) + ' GB' if item.get('size') else 'NA'
					listitem.setProperty('fuzzybritches.source_dict', jsdumps([item]))
					listitem.setProperty('fuzzybritches.debrid', self.debrid_name(item.get('debrid')))
					listitem.setProperty('fuzzybritches.debridabrv', self.debrid_abv(item.get('debrid')))
					listitem.setProperty('fuzzybritches.provider', item.get('provider').upper())
					listitem.setProperty('fuzzybritches.plexsource', item.get('plexsource', '').upper())
					listitem.setProperty('fuzzybritches.source', item.get('source').upper())
					listitem.setProperty('fuzzybritches.seeders', str(item.get('seeders')))
					listitem.setProperty('fuzzybritches.hash', item.get('hash', 'N/A'))
					listitem.setProperty('fuzzybritches.name', item.get('name'))
					listitem.setProperty('fuzzybritches.quality', quality.upper())
					listitem.setProperty('fuzzybritches.quality_icon', quality_icon)
					listitem.setProperty('fuzzybritches.url', item.get('url'))
					listitem.setProperty('fuzzybritches.extra_info', extra_info)
					listitem.setProperty('fuzzybritches.size_label', size_label)
					listitem.setProperty('fuzzybritches.count', '%02d.)' % count)
					listitem.setProperty('fuzzybritches.providerhighlight', str(providerHighlight))
					listitem.setProperty('fuzzybritches.quality_icon1', str(quality1_icon))
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
		if self.meta is None: return
		try:
			if 'tvshowtitle' in self.meta and 'season' in self.meta and 'episode' in self.meta: 
				self.setProperty('fuzzybritches.seas_ep', 'S%02dE%02d' % (int(self.meta['season']), int(self.meta['episode'])))
				self.setProperty('fuzzybritches.season', str(self.meta.get('season', '')))
				self.setProperty('fuzzybritches.episode', str(self.meta.get('episode', '')))
			if self.meta.get('title'): self.setProperty('fuzzybritches.title', self.meta.get('title'))
			if self.meta.get('season_poster'):	self.setProperty('fuzzybritches.poster', self.meta.get('season_poster', ''))
			else: self.setProperty('fuzzybritches.poster', self.meta.get('poster', ''))
			if self.meta.get('fanart'): self.setProperty('fuzzybritches.poster1', self.meta.get('fanart', ''))
			else: self.setProperty('fuzzybritches.poster1', 'common/fanart.jpg')
			self.setProperty('fuzzybritches.clearlogo', self.meta.get('clearlogo', ''))
			self.setProperty('fuzzybritches.plot', self.meta.get('plot', ''))
			if self.meta.get('premiered'):
				pdate = str(self.meta.get('premiered'))[:4]
				self.setProperty('fuzzybritches.year', str(pdate))
			new_date = tools.convert_time(stringTime=str(self.meta.get('premiered', '')), formatInput='%Y-%m-%d', formatOutput='%m-%d-%Y', zoneFrom='utc', zoneTo='utc')
			self.setProperty('fuzzybritches.premiered', new_date)
			if self.meta.get('mpaa'): self.setProperty('fuzzybritches.mpaa', self.meta.get('mpaa'))
			else: self.setProperty('fuzzybritches.mpaa', 'NA ')
			if self.meta.get('duration'):
				duration = int(self.meta.get('duration')) / 60
				self.setProperty('fuzzybritches.duration', str(int(duration)))
			else: self.setProperty('fuzzybritches.duration', 'NA ')
			self.setProperty('fuzzybritches.uncached_results', 'true' if self.uncached else 'false')
			self.setProperty('fuzzybritches.total_results', self.total_results)
			self.setProperty('fuzzybritches.highlight.color', self.highlight_color)
			self.setProperty('fuzzybritches.dialog.color', self.dialogColor)
			self.setProperty('fuzzybritches.fanartdefault', addonFanart())
			if getSetting('sources.select.fanartBG') == 'true':
				self.setProperty('fuzzybritches.fanartBG', '1')
			else:
				self.setProperty('fuzzybritches.fanartBG', '0')
			if getSetting('sources.backbutton') == 'true':
				self.setProperty('fuzzybritches.sourcebackbutton', '1')
			else:
				self.setProperty('fuzzybritches.sourcebackbutton', '0')
			if getSetting('sources.highlightmethod') == '1':
				self.setProperty('fuzzybritches.useprovidercolors', '1')
				self.setProperty('fuzzybritches.realdebridcolor', self.realdebridHighlightColor)
				self.setProperty('fuzzybritches.alldebridcolor', self.alldebridHighlightColor)
				self.setProperty('fuzzybritches.premiumizecolor', self.premiumizeHighlightColor)
				self.setProperty('fuzzybritches.plexcolor', self.plexHighlightColor)
				self.setProperty('fuzzybritches.easynewscolor', self.easynewsHighlightColor)
				self.setProperty('fuzzybritches.gdrivecolor', self.gdriveHighlightColor)
				self.setProperty('fuzzybritches.filepursuitcolor', self.filePursuitHighlightColor)
				self.setProperty('fuzzybritches.torboxcolor', self.torboxHighlightColor)
				self.setProperty('fuzzybritches.easydebridcolor', self.easyDebridHighlightColor)
				self.setProperty('fuzzybritches.offcloudcolor', self.offcloudHighlightColor)
				
				if getSetting('sources.usecoloricons') == 'true':
					self.setProperty('fuzzybritches.usecoloricons', '1')
				else:
					self.setProperty('fuzzybritches.usecoloricons', '0')
			else:
				self.setProperty('fuzzybritches.useprovidercolors', '0')
				self.setProperty('fuzzybritches.usecoloricons', '0')
		except:
			from resources.lib.modules import log_utils
			log_utils.error()

	def load_uncachedTorrents(self):
		try:
			from resources.lib.windows.uncached_results import UncachedResultsXML
			from resources.lib.modules.control import addonPath, addonId
			window = UncachedResultsXML('uncached_results.xml', addonPath(addonId()), uncached=self.uncached, meta=self.meta, colors=self.colors)
			window.run()
		except:
			from resources.lib.modules import log_utils
			log_utils.error()