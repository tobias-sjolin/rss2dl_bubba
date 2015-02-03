#!/usr/bin/python

# rss2dl.py will look at an RSS feed and download programs that you want.
# Change the sources list to monitor the RSS feeds you want to check
# Run this program from cron whenever you want (you can try to optimize it to
# the times the programs will normally show up on the rss feeds, or just once
# every 6 hours.

## Any specific filetype you don't want to download
blacklist = ['WEB-DL','(Indi)','DD5']

## The link to our own tvtorrents rss-feed
#sources = ['http://www.tvtorrents.com/mytaggedRSS?digest=XXXXX']  - TVTorrents discontinued...
#Recent torrents
#sources = ['http://freshon.tv/rss.php?feed=dl&c[]=545&c[]=601&c[]=6221&c[]=386&c[]=577&c[]=313&c[]=55']
#

__author__ = 'Baruch Even <baruch@ev-en.org> and Mkay'
__version__ = '1.0.1 Bubba edition'

import feedparser, re, urlparse, urllib2, ConfigParser
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

#Read our config file for input
config = ConfigParser.SafeConfigParser()
config.read("conf_rss2dl.cnf")
#Passkey
passkey = config.get('rss2dl', 'passkey')
print 'Passkey: ' + passkey
## The Bubba user you wish to download the torrent as
user = config.get('rss2dl', 'user')
print 'User: ' + user
#Set the Dir to download to
dir = '/home/' + user + '/torrents'
print 'Dir: ' +dir
#Change this to 1 to see all the logging
verbose = config.getint('rss2dl', 'verbose')
print 'Verbose: ' + str(verbose)
#Number of hours to download torrents for
timeLimitHours = config.getint('rss2dl', 'timeLimitHours')
print 'timeLimitHours: ' + str(timeLimitHours)
#Episode download only (no full Season torrents)
episodeOnly = config.getint('rss2dl', 'episodeOnly')
print 'EpisodeOnly: ' + str(episodeOnly)
sources = ['http://freshon.tv/rss.php?feed=dl&c[]=545&c[]=601&c[]=6221&c[]=386&c[]=577&c[]=313&c[]=552&passkey=' + passkey]
for src in sources:
	rss = feedparser.parse(src)
        if verbose:
	    print 'PRINT rss '
            print rss
            print 'PRINT rss.entries'
            print rss.entries
	for entry in rss.entries:
            if verbose:
                print 'PRINT title' + entry['title']
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
                    print 'NOW: ' + str(datetime.now())
                    print 'PubDate: ' + str(entry['updated'])                
                    print 'PubDate fixed: ' + str(date_object)
                if (datetime.now() - date_object) > timedelta(hours = timeLimitHours) and stop == 0:
                    print entry['title'] + ' too old to download (Age: ' + str(datetime.now()-date_object) + ' since ' + str(date_object) + ')'
                    stop = 1
                a = re.compile("^([a-zA-Z0-9.]*)\.S([0-9]{1,2})E([0-9]{1,2}).*$")
                if stop == 0 and episodeOnly and not a.match(entry['title']):
                    print entry['title'] + ' Not an episode, no download'
                    stop = 1
                #If everything is okey then download the link provided
		if stop == 0:
		    try:
		        dlfile(entry['link'])
			print 'Downloading ' + entry['title']
		    except Exception,e:
	                print e
					
					
					
					
