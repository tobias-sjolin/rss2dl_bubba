#!/usr/bin/python

# rss2dl.py will look at an RSS feed and download programs that you want.
# Change the progs list to have the names of the programs you want to download
# Change the sources list to monitor the RSS feeds you want to check
# Run this program from cron whenever you want (you can try to optimize it to
# the times the programs will normally show up on the rss feeds, or just once
# every 6 hours.

## The Bubba user you wish to download the torrent as
user = 'tobias'

## The shows you would like to download,
#progs = ['How I Met Your Mother -', 'The Big Bang Theory -','Community']

## Any specific filetype you don't want to download
#blacklist = '720p .mkv'
blacklist = ['WEB-DL','(Indi)','DD5']

## The link to our own tvtorrents rss-feed
#sources = ['http://www.tvtorrents.com/RssServlet?digest=XXXXX']
# Favourite torrents
#sources = ['http://www.tvtorrents.com/mytaggedRSS?digest=XXXXX']  - TVTorrents discontinued...
#Recent torrents
#sources = ['http://www.tvtorrents.com/RssServlet?digest=XXXXX']
sources = ['http://freshon.tv/rss.php?feed=dl&c[]=545&c[]=601&c[]=6221&c[]=386&c[]=577&c[]=313&c[]=552&passkey=XXXX']
#
## Do not edit beyond this line
#


dir = '/home/' + user + '/torrents'
#Change this to 1 to see all the logging
verbose = 0
#Number of hours to download torrents for
timeLimitHours = 4

__author__ = 'Baruch Even <baruch@ev-en.org> and Mkay'
__version__ = '1.0.1 Bubba edition'

import feedparser, re, urlparse, urllib2
from os.path import basename, join, exists
from datetime import datetime, timedelta

def dlfile(link):
	url = entry['title'] + ".torrent"
	path = join(dir, basename(url))
	if exists(path):
		return

        # add a header to define a custom User-Agent
        req = urllib2.Request(link)
        req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0')
        req.add_header('Cookie','__cfduid=dfb11515254ea45b882cc39409b4372af1390494025217')

	torrent = urllib2.urlopen(req).read()

        f = file(path, 'wb')
        #os.chmod(name, 0600)
	f.write(torrent)
	f.close()

for src in sources:
	rss = feedparser.parse(src)
        if verbose:
	    print 'PRINT rss '
            print rss
            print 'PRINT rss.entries'
            print rss.entries
	for entry in rss.entries:
            if verbose:
                print 'PRINT title'
                print entry['title']
	    stop = 0
            #Check if the title contains any of the blacklist words
            for blist in blacklist:
		if blist in entry['title']:
		    print entry['title'] + ' in blacklist'
		    stop = 1	
                #Check the date to only download torrents for the last X provided hours.
                date = entry['updated']
                #Python version I am running does not support offest (%z) so need to cut that out
                date = date[:-6]
                #Convert string to datetime
                date_object = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
                if verbose:
                    print 'PRINT now '
                    print datetime.now()
                    print 'PRINT pubDate '
                    print entry['updated']                
                    print 'PRINT pubDate fixed '
                    print date_object
                if (datetime.now() - date_object) > timedelta(hours = timeLimitHours) and stop == 0:
                    print entry['title'] + ' too old to download'
                    print(datetime.now()-date_object)
                    print date_object
                    stop = 1
                #If everything is okey then download the link provided
		if stop == 0:
		    try:
		        dlfile(entry['link'])
			print 'Downloading ' + entry['title']
		    except Exception,e:
	                print e
					
					
					
					
