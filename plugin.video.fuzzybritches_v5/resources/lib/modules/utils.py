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

from json import loads as jsloads


def json_load_as_str(file_handle):
	return byteify(jsloads(file_handle, object_hook=byteify), ignore_dicts=True)

def json_loads_as_str(json_text):
	return byteify(jsloads(json_text, object_hook=byteify), ignore_dicts=True)

def byteify(data, ignore_dicts=False):
	if isinstance(data, str):
		return data
	if isinstance(data, list):
		return [byteify(item, ignore_dicts=True) for item in data]
	if isinstance(data, dict) and not ignore_dicts:
		return dict([(byteify(key, ignore_dicts=True), byteify(value, ignore_dicts=True)) for key, value in iter(data.items())])
	return data