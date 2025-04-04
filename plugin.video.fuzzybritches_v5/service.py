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

from resources.lib.modules import control, log_utils
from sys import version_info, platform as sys_platform
from threading import Thread
import time
from datetime import timedelta
window = control.homeWindow
pythonVersion = '{}.{}.{}'.format(version_info[0], version_info[1], version_info[2])
plugin = 'plugin://plugin.video.fuzzybritches_v5/'
LOGINFO = log_utils.LOGINFO
LOGDEBUG = log_utils.LOGDEBUG

properties = [
	'context.fuzzybritches.settings',
	'context.fuzzybritches.addtoLibrary',
	'context.fuzzybritches.addtoFavourite',
	'context.fuzzybritches.playTrailer',
	'context.fuzzybritches.playTrailerSelect',
	'context.fuzzybritches.traktManager',
	'context.fuzzybritches.clearProviders',
	'context.fuzzybritches.clearBookmark',
	'context.fuzzybritches.rescrape',
	'context.fuzzybritches.playFromHere',
	'context.fuzzybritches.autoPlay',
	'context.fuzzybritches.sourceSelect',
	'context.fuzzybritches.findSimilar',
	'context.fuzzybritches.browseSeries',
	'context.fuzzybritches.browseEpisodes']

class CheckSettingsFile:
	def run(self):
		try:
			control.log('[ plugin.video.fuzzybritches_v5 ]  CheckSettingsFile Service Starting...', LOGINFO)
			window.clearProperty('fuzzybritches_settings')
			profile_dir = control.dataPath
			if not control.existsPath(profile_dir):
				success = control.makeDirs(profile_dir)
				if success: control.log('%s : created successfully' % profile_dir, LOGINFO)
			else: control.log('%s : already exists' % profile_dir, LOGINFO)
			settings_xml = control.joinPath(profile_dir, 'settings.xml')
			if not control.existsPath(settings_xml):
				control.setSetting('trakt.message2', '')
				control.log('%s : created successfully' % settings_xml, LOGINFO)
			else: control.log('%s : already exists' % settings_xml, LOGINFO)
			return control.log('[ plugin.video.fuzzybritches_v5 ]  Finished CheckSettingsFile Service', LOGINFO)
		except:
			log_utils.error()

class SettingsMonitor(control.monitor_class):
	def __init__ (self):
		control.monitor_class.__init__(self)
		control.refresh_playAction()
		control.refresh_libPath()
		window.setProperty('fuzzybritches.debug.reversed', str(control.setting('debug.reversed')))
		window.setProperty('fuzzybritches.updateSettings', 'true')
		for id in properties:
			if control.setting(id) == 'true':
				window.setProperty(id, 'true')
				#xbmc.log('[ plugin.video.fuzzybritches_v5.context ]  menu item enabled: {0}'.format(id), LOGINFO)
		control.log('[ plugin.video.fuzzybritches_v5 ]  Settings Monitor Service Starting...', LOGINFO)

	def onSettingsChanged(self):
		if window.getProperty('fuzzybritches.updateSettings') != 'true':
			return control.log('[ plugin.video.fuzzybritches_v5 ]  Settings Monitor is off.', LOGINFO)
		window.setProperty('fuzzybritches.updateSettings','false')

		try:
			window.clearProperty('fuzzybritches_settings') # Kodi callback when the addon settings are changed
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception clearing settings property...', LOGDEBUG)

		try:
			control.refresh_playAction()
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception making refreshing playAction...', LOGDEBUG)
		try:
			control.refresh_libPath()
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception refreshing libpath...', LOGDEBUG)
		#try:
			#control.checkPlayNextEpisodes()
		#except:
			#control.log('[ plugin.video.fuzzybritches_v5 ]  Exception checking playnext episodes...', LOGDEBUG)
		try:
			control.refresh_debugReversed()
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception checking debug reversed', LOGDEBUG)
		try:
			control.setContextColors()
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception setting context colors...', LOGDEBUG)
		try:
			control.checkModules()
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception checking modules...', LOGDEBUG)
		try:
			control.sleep(50)
			control.make_settings_dict()
			window.setProperty('fuzzybritches.updateSettings','true')
		except:
			control.log('[ plugin.video.fuzzybritches_v5 ]  Exception making settings dict...', LOGDEBUG)
		try:
			for id in properties:
				if control.setting(id) == 'true':
					window.setProperty(id, 'true')
				else:
					window.clearProperty(id)
					#xbmc.log('[ plugin.video.fuzzybritches_v5.context ]  menu item disabled: {0}'.format(id), LOGINFO)
		except:
			log_utils.error()

class SyncMyAccounts:
	def run(self):
		control.log('[ plugin.video.fuzzybritches_v5 ]  Sync Accounts with Scraper Starting...', LOGINFO)
		control.syncAccounts()
		return control.log('[ plugin.video.fuzzybritches_v5 ]  Finished Sync with Scraper', LOGINFO)

class SyncMovieLibrary:
	def run(self):
		if control.setting('library.cachesimilar') == 'true':
			control.log('[ plugin.video.fuzzybritches_v5 ]  Sync Library Movies with FuzzyBritches...', LOGINFO)
			from resources.lib.modules import library
			library.lib_tools().cacheLibraryforSimilar() 
			return control.log('[ plugin.video.fuzzybritches_v5 ]  Sync Library Movies with FuzzyBritches Done', LOGINFO)
		else:
			return

class checkAutoStart:
	def run(self):
		control.log('[ plugin.video.fuzzybritches_v5 ]  Checking for AutoStart....', LOGINFO)
		if control.setting('fuzzybritches.autostart') == 'true': 
			control.execute('RunAddon(plugin.video.fuzzybritches_v5)')
		return control.log('[ plugin.video.fuzzybritches_v5 ]  Finished AutoStart Check', LOGINFO)


class ReuseLanguageInvokerCheck:
	def run(self):
		control.log('[ plugin.video.fuzzybritches_v5 ]  ReuseLanguageInvokerCheck Service Starting...', LOGINFO)
		try:
			#import xml.etree.ElementTree as ET
			from xml.dom.minidom import parse as mdParse
			from resources.lib.modules.language_invoker import gen_file_hash
			addon_xml = control.joinPath(control.addonPath('plugin.video.fuzzybritches_v5'), 'addon.xml')
			#tree = ET.parse(addon_xml)
			#root = tree.getroot()
			current_addon_setting = control.addon('plugin.video.fuzzybritches_v5').getSetting('reuse.languageinvoker')
			#try: current_xml_setting = [str(i.text) for i in root.iter('reuselanguageinvoker')][0]
			try:
				tree = mdParse(addon_xml)
				reuse = tree.getElementsByTagName("reuselanguageinvoker")[0]
				current_xml_setting = reuse.firstChild.data
			except: return control.log('[ plugin.video.fuzzybritches_v5 ]  ReuseLanguageInvokerCheck failed to get settings.xml value', LOGINFO)
			if current_addon_setting == '':
				current_addon_setting = 'true'
				control.setSetting('reuse.languageinvoker', current_addon_setting)
			if current_xml_setting == current_addon_setting:
				return control.log('[ plugin.video.fuzzybritches_v5 ]  ReuseLanguageInvokerCheck Service Finished', LOGINFO)
			control.okDialog(message='%s\n%s' % (control.lang(33023), control.lang(33020)))
			#item.text = current_addon_setting
			tree.getElementsByTagName("reuselanguageinvoker")[0].firstChild.data = current_addon_setting
			hash_start = gen_file_hash(addon_xml)
			newxml = str(tree.toxml())[22:] #for some reason to xml adds this so we remove it."<?xml version="1.0" ?>"
			with open(addon_xml, "w") as f:
				f.write(newxml)
			#tree.write(addon_xml)
			hash_end = gen_file_hash(addon_xml)
			control.log('[ plugin.video.fuzzybritches_v5 ]  ReuseLanguageInvokerCheck Service Finished', LOGINFO)
			if hash_start != hash_end:
				current_profile = control.infoLabel('system.profilename')
				control.execute('LoadProfile(%s)' % current_profile)
			else: control.okDialog(title='default', message=33022)
			return
		except:
			log_utils.error()

class AddonCheckUpdate:
	def run(self):
		control.log('[ plugin.video.fuzzybritches_v5 ]  Addon checking available updates', LOGINFO)
		try:
			import re
			import requests
			local_version = control.getFuzzyBritchesVersion() # 5 char max so pre-releases do try to compare more chars than github version 6.5.941
			if len(local_version) > 6: #test version
				repo_xml = requests.get('https://raw.githubusercontent.com/fuzzybritcheskodi/fuzzybritcheskodi/master/matrix/plugin.video.fuzzybritches_v5/addon.xml')
			else:
				repo_xml = requests.get('https://raw.githubusercontent.com/fuzzybritchesplug/fuzzybritchesplug.github.io/master/matrix/plugin.video.fuzzybritches_v5/addon.xml')
			if not repo_xml.status_code == 200:
				return control.log('[ plugin.video.fuzzybritches_v5 ]  Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, LOGINFO)
			repo_version = re.findall(r'<addon id=\"plugin.video.fuzzybritches_v5\".+version=\"(\d*.\d*.\d*)\"', repo_xml.text)[0]
			def check_version_numbers(current, new): # Compares version numbers and return True if github version is newer
				current = current.split('.')
				new = new.split('.')
				step = 0
				for i in current:
					if int(new[step]) > int(i): return True
					if int(i) > int(new[step]): return False
					if int(i) == int(new[step]):
						step += 1
						continue
				return False
			if check_version_numbers(local_version, repo_version):
				while control.condVisibility('Library.IsScanningVideo'):
					control.sleep(10000)
				control.log('[ plugin.video.fuzzybritches_v5 ]  A newer version is available. Installed Version: v%s, Repo Version: v%s' % (local_version, repo_version), LOGINFO)
				control.notification(message=control.lang(35523) % repo_version)
			return control.log('[ plugin.video.fuzzybritches_v5 ]  Addon update check complete', LOGINFO)
		except:
			log_utils.error()

class VersionIsUpdateCheck:
	def run(self):
		try:
			from resources.lib.database import cache
			isUpdate = False
			oldVersion, isUpdate = cache.update_cache_version()
			if isUpdate:
				window.setProperty('fuzzybritches.updated', 'true')
				curVersion = control.getFuzzyBritchesVersion()
				clearDB_version = '6.5.58' # set to desired version to force any db clearing needed
				do_cacheClear = (int(oldVersion.replace('.', '')) < int(clearDB_version.replace('.', '')) <= int(curVersion.replace('.', '')))
				if do_cacheClear:
					clr_fanarttv = False
					cache.clrCache_version_update(clr_providers=False, clr_metacache=True, clr_cache=True, clr_search=False, clr_bookmarks=False)
					from resources.lib.database import traktsync
					clr_traktSync = {'bookmarks': False, 'hiddenProgress': False, 'liked_lists': False, 'movies_collection': False, 'movies_watchlist': False, 'popular_lists': False,
											'public_lists': False, 'shows_collection': False, 'shows_watchlist': False, 'trending_lists': False, 'user_lists': False, 'watched': False}
					cleared = traktsync.delete_tables(clr_traktSync)
					if cleared:
						control.notification(message='Forced traktsync clear for version update complete.')
						control.log('[ plugin.video.fuzzybritches_v5 ]  Forced traktsync clear for version update complete.', LOGINFO)
					if clr_fanarttv:
						from resources.lib.database import fanarttv_cache
						cleared = fanarttv_cache.cache_clear()
						control.notification(message='Forced fanarttv.db clear for version update complete.')
						control.log('[ plugin.video.fuzzybritches_v5 ]  Forced fanarttv.db clear for version update complete.', LOGINFO)
				control.setSetting('trakt.message2', '') # force a settings write for any added settings that may have been added in new version
				control.log('[ plugin.video.fuzzybritches_v5 ]  Forced new User Data settings.xml saved', LOGINFO)
				control.log('[ plugin.video.fuzzybritches_v5 ]  Plugin updated to v%s' % curVersion, LOGINFO)
		except:
			log_utils.error()

class SyncTraktCollection:
	def run(self):
		control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Collection Sync Import Disabled...', LOGINFO)
		#control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Collection Sync Starting...', LOGINFO)
		#control.execute('RunPlugin(%s?action=library_tvshowsToLibrarySilent&url=traktcollection)' % plugin)
		#control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Collection Sync TV Shows Complete', LOGINFO)
		#control.execute('RunPlugin(%s?action=library_moviesToLibrarySilent&url=traktcollection)' % plugin)
		#control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Collection Sync Movies Complete', LOGINFO)
		#control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Collection Sync Complete', LOGINFO)

class LibraryService:
	def run(self):
		try:
			library_hours = float(control.setting('library.import.hours'))
		except:
			library_hours = int(6)
		control.log('[ plugin.video.fuzzybritches_v5 ]  Library Update Service Starting (Runs Every %s Hours)...' % library_hours,  LOGINFO)
		from resources.lib.modules import library
		library.lib_tools().service() # method contains control.monitor().waitForAbort() while loop every 6hrs

class SyncTraktService:
	def run(self):
		service_syncInterval = control.setting('trakt.service.syncInterval') or '15'
		control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Sync Service Starting (sync check every %s minutes)...' % service_syncInterval, LOGINFO)
		from resources.lib.modules import trakt
		trakt.trakt_service_sync() # method contains "control.monitor().waitForAbort()" while loop every "service_syncInterval" minutes

try:
	testFuzzyBritches = False
	kodiVersion = control.getKodiVersion(full=True)
	addonVersion = control.addon('plugin.video.fuzzybritches_v5').getAddonInfo('version')
	if len(str(control.getFuzzyBritchesVersion())) > 6:
		repoVersion = control.addon('repository.fuzzybritchestest').getAddonInfo('version')
		repoName = 'repository.fuzzybritchestest'
		testFuzzyBritches = True
	else:
		try:
			repoVersion = control.addon('repository.fuzzybritches').getAddonInfo('version')
			repoName = 'repository.fuzzybritches'
		except:
			repoVersion = 'unknown'
			repoName = 'Unknown Repo'

	log_utils.log('########   CURRENT FuzzyBritches VERSIONS REPORT   ########', level=LOGINFO)
	if testFuzzyBritches == True:
		log_utils.log('########   TEST FuzzyBritches Version   ########', level=LOGINFO)
	log_utils.log('##   Platform: %s' % str(sys_platform), level=LOGINFO)
	log_utils.log('##   Kodi Version: %s' % str(kodiVersion), level=LOGINFO)
	log_utils.log('##   python Version: %s' % pythonVersion, level=LOGINFO)
	log_utils.log('##   plugin.video.fuzzybritches_v5 Version: %s' % str(addonVersion), level=LOGINFO)
	log_utils.log('##   %s Version: %s' % (str(repoName), str(repoVersion)), level=LOGINFO)
	log_utils.log('######   FuzzyBritches SERVICE ENTERING KEEP ALIVE   #####', level=LOGINFO)
except:
	log_utils.log('## ERROR GETTING FuzzyBritches VERSION - Missing Repo or failed Install ', level=LOGINFO)

def getTraktCredentialsInfo():
	username = control.setting('trakt.user.name').strip()
	token = control.setting('trakt.user.token')
	refresh = control.setting('trakt.refreshtoken')
	if (username == '' or token == '' or refresh == ''): return False
	return True

class PremAccntNotification:
	def run(self):
		from datetime import datetime
		from resources.lib.debrid import alldebrid
		from resources.lib.debrid import premiumize
		from resources.lib.debrid import realdebrid
		control.log('[ plugin.video.fuzzybritches_v5 ] Debrid Account Expiry Notification Service Starting...', LOGINFO)
		self.duration = [(15, 10), (11, 7), (8, 4), (5, 2), (3, 0)]
		if control.setting('alldebridusername') != '' and control.setting('alldebridexpirynotice') == 'true':
			try:
				account_info = alldebrid.AllDebrid().account_info()['user']
			except:
				account_info = None
				from resources.lib.modules import log_utils
				log_utils.error()
			if account_info:
				if not account_info['isSubscribed']:
					# log_utils.log('AD account_info = %s' % account_info, log_utils.LOGINFO)
					try:
						expires = datetime.fromtimestamp(account_info['premiumUntil'])
					except:
						expires = datetime.today()-timedelta(days=1)
						control.notification(message='AllDebrid Account has no expiration. Invalid or free account.', icon=control.joinPath(control.artPath(), 'alldebrid.png'))
					days_remaining = (expires - datetime.today()).days # int
					if days_remaining >= 0:
						if self.withinRangeCheck('alldebrid', days_remaining):
							control.notification(message='AllDebrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'alldebrid.png'))

		if control.setting('premiumizeusername') != '' and control.setting('premiumizeexpirynotice') == 'true':
			account_info = premiumize.Premiumize().account_info()
			if account_info:
				# log_utils.log('PM account_info = %s' % account_info, log_utils.LOGINFO)
				try: 
					expires = datetime.fromtimestamp(account_info['premium_until'])
				except:
					expires = datetime.today()-timedelta(days=1)
					control.notification(message='Premiumize.me Account has no expiration. Invalid or free account.', icon=control.joinPath(control.artPath(), 'premiumize.png'))
				days_remaining = (expires - datetime.today()).days # int
				if days_remaining >= 0:
					if self.withinRangeCheck('premiumize', days_remaining):
						control.notification(message='Premiumize.me Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'premiumize.png'))

		if control.setting('realdebridusername') != '' and control.setting('realdebridexpirynotice') == 'true':
			account_info = realdebrid.RealDebrid().account_info()
			if account_info:
				# log_utils.log('RD account_info = %s' % account_info, log_utils.LOGINFO)
				FormatDateTime = "%Y-%m-%dT%H:%M:%S.%fZ"
				try: expires = datetime.strptime(account_info['expiration'], FormatDateTime)
				except: 
					try: expires = datetime(*(time.strptime(account_info['expiration'], FormatDateTime)[0:6]))
					except: 
						expires = datetime.today()-timedelta(days=1)
						control.notification(message='Real-Debrid Account has no expiration. Invalid or free account.', icon=control.joinPath(control.artPath(), 'realdebrid.png'))
				days_remaining = (expires - datetime.today()).days # int
				if days_remaining >= 0:
					if self.withinRangeCheck('realdebrid', days_remaining):
						control.notification(message='Real-Debrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'realdebrid.png'))

	def withinRangeCheck(self, debrid_provider, days_remaining):
		if days_remaining < 15:
			try: current_notification_range = int(control.setting('%s.notification.range' % debrid_provider))
			except: current_notification_range = 5
			for index, day_range in enumerate(self.duration):
				if day_range[0] > days_remaining > day_range[1] and current_notification_range != index:
					control.setSetting('%s.notification.range' % debrid_provider, str(index))
					return True
			return False
		else:
			control.setSetting('%s.notification.range' % debrid_provider, '')
			return False

def main():
	while not control.monitor.abortRequested():
		control.log('[ plugin.video.fuzzybritches_v5 ]  Service Started', LOGINFO)
		schedTrakt = None
		libraryService = None
		CheckSettingsFile().run()
		SyncMyAccounts().run()
		PremAccntNotification().run()
		ReuseLanguageInvokerCheck().run()
		SyncMovieLibrary().run()
		#control.checkPlayNextEpisodes()
		if control.setting('library.service.update') == 'true':
			libraryService = Thread(target=LibraryService().run)
			libraryService.start()
		if control.setting('general.checkAddonUpdates') == 'true':
			AddonCheckUpdate().run()
		VersionIsUpdateCheck().run()
		checkAutoStart().run()

		syncTraktService = Thread(target=SyncTraktService().run) # run service in case user auth's trakt later, sync will loop and do nothing without valid auth'd account
		syncTraktService.start()

		# if getTraktCredentialsInfo():
		# 	if control.setting('autoTraktOnStart') == 'true':
		# 		SyncTraktCollection().run()
		# 	if int(control.setting('schedTraktTime')) > 0:
		# 		import threading
		# 		log_utils.log('#################### STARTING TRAKT SCHEDULING ################', level=LOGINFO)
		# 		log_utils.log('#################### SCHEDULED TIME FRAME '+ control.setting('schedTraktTime')  + ' HOURS ###############', level=LOGINFO)
		# 		timeout = 3600 * int(control.setting('schedTraktTime'))
		# 		schedTrakt = threading.Timer(timeout, SyncTraktCollection().run) # this only runs once at the designated interval time to wait...not repeating
		# 		schedTrakt.start()
		break
	SettingsMonitor().waitForAbort()
	# start monitoring settings changes events
	control.log('[ plugin.video.fuzzybritches_v5 ]  Settings Monitor Service Stopping...', LOGINFO)
	del syncTraktService # prob does not kill a running thread
	control.log('[ plugin.video.fuzzybritches_v5 ]  Trakt Sync Service Stopping...', LOGINFO)
	if libraryService:
		del libraryService # prob does not kill a running thread
		control.log('[ plugin.video.fuzzybritches_v5 ]  Library Update Service Stopping...', LOGINFO)
	if schedTrakt:
		schedTrakt.cancel()
	control.log('[ plugin.video.fuzzybritches_v5 ]  Service Stopped', LOGINFO)

main()