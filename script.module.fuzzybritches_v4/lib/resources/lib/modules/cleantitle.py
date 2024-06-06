# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v4
# Addon id: plugin.video.fuzzybritches_v4
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import re
import urllib
import unicodedata

from string import printable
from urllib.parse import unquote

def get(title):
    if title is None: return
    try:
        if not type(title) == str: #this should only work well with int's
            title = str(title)
    except:
        pass
    title = re.sub(r'&#(\d+);', '', title)
    title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace(r'&quot;', '\"').replace(r'&amp;', '&').replace(r'–', '-').replace(r'!', '')
    title = re.sub(r'\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def get_title(title):
    if title is None: return

    try:
        title = str(title)
    except:
        pass
    title = urllib.parse.unquote(title).lower()
    title = re.sub('[^a-z0-9 ]+', ' ', title)
    title = re.sub(' {2,}', ' ', title)
    return title


def geturl(title):
    if title is None: return
    try:
        title = str(title)
    except:
        pass
    title = title.lower()
    title = title.rstrip()
    try: title = title.translate(None, ':*?"\'\.<>|&!,')
    except: title = title.translate(str.maketrans('', '', ':*?"\'\.<>|&!,'))
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    title = title.replace('–', '-')
    title = title.replace('!', '')
    return title


def get_url(title):
    if title is None:
        return
    try:
        title = str(title)
    except:
        pass
    title = title.replace(' ', '%20').replace('–', '-').replace('!', '')
    return title


def get_gan_url(title):
    if title is None:
        return
    title = title.lower()
    title = title.replace('-','+')
    title = title.replace(' + ', '+-+')
    title = title.replace(' ', '%20')
    return title


def get_query_(title):
    if title is None: return
    try:
        title = str(title)
    except:
        pass
    title = title.replace(' ', '_').replace("'", "_").replace('-', '_').replace('–', '_').replace(':', '').replace(',', '').replace('!', '')
    return title.lower()

def get_simple(title):
    if title is None:
        return
    try:
        title = str(title)
    except:
        pass
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('–', '-')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    title = re.sub(r'<.*?>', '', title, count=0)
    return title


def getsearch(title):
    if title is None: return
    try:
        title = str(title)
    except:
        pass
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('–', '-')
    title = re.sub('\\\|/|-|–|:|;|!|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title is None: return
    try:
        title = str(title)
    except:
        pass
    title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ').replace('–', ' ').replace('!', '')
    return title


def get_query(title):
    if title is None: return
    try:
        title = str(title)
    except:
        pass
    title = title.replace(':', '').replace("'", "").lower()
    return title


def normalize(title):
    try:
        return u''.join(c for c in unicodedata.normalize('NFKD', str(title)) if c in printable)
    except:
        return title

def clean_search_query(url):
    url = url.replace('-','+').replace(' ', '+').replace('–', '+').replace('!', '')
    return url