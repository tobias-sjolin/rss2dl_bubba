#!/usr/bin/python

# rss2dl.py will look at an RSS feed and download programs that you want.
# Change the progs list to have the names of the programs you want to download
# Change the sources list to monitor the RSS feeds you want to check
# Run this program from cron whenever you want (you can try to optimize it to
# the times the programs will normally show up on the rss feeds, or just once
# every 6 hours.

## The user you wish to download the torrent as
user = 'tobias'

## The shows you would like to download,
progs = ['How I Met Your Mother -', 'The Big Bang Theory -','Community']

## Any specific filetype you don't want to download
blacklist = '720p .mkv'

## The link to our own tvtorrents rss-feed
##sources = ['http://www.tvtorrents.com/RssServlet?digest=XXXXX']
sources = ['http://www.tvtorrents.com/RssServlet?digest=XXXXX']

#
## Do not edit beyond this line
#


dir = '/home/' + user + '/torrents'

__author__ = 'Baruch Even <baruch@ev-en.org> and Mkay'
__version__ = '1.0.1 Bubba edition'

import feedparser, re, urlparse, urllib
from os.path import basename, join, exists

def dlfile(link):
	url = entry['title'] + ".torrent"
	path = join(dir, basename(url))
	if exists(path):
		return
		
	u = urllib.urlopen(link)
	torrent = u.read()
	f = file(path, 'wb')
	f.write(torrent)
	f.close()

title_re = re.compile(r'(.*?) ((?:\d+x\d+)|(?:\d+\.\d+\.\d+))(.*)')#(.*?) ?\((.*)\)')
for src in sources:
	rss = feedparser.parse(src)
	for entry in rss.entries:
		m = title_re.match(entry['title'])
		
		if not m:
			continue
		
		if m.group(1) in progs:
			if blacklist not in m.group(3):
				try:
					dlfile(entry['link'])
					print 'Downloading ' + entry['title']
				except Exception,e:
					print e
					
					
					
					
