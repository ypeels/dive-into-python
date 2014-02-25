"""Extract list of URLs in a web page

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

from sgmllib import SGMLParser

class URLLister(SGMLParser):
	def reset(self):                                        # called by SGMLParser.__init__()
		SGMLParser.reset(self)                                  # so put any (re-)initialization code here!
		self.urls = []

	def start_a(self, attrs):                               # called by SGMLParser (by instrospection?) upon finding <a>
		href = [v for k, v in attrs if k=='href']           # don't worry about case-sensitivity: SGMLParser converts attribute names to lowercase
		if href:
			self.urls.extend(href)

if __name__ == "__main__":
	import urllib                                           # get info about and retrieve Internet URLs
	#usock = urllib.urlopen("http://diveintopython.org/")   # Updated domain name as of 2/2014
	usock = urllib.urlopen("http://diveintopython.net/")    # cf. file API
	parser = URLLister()
	parser.feed(usock.read())                               # Example 8.7: feeds HTML into parser
	parser.close()                                          # flush parser's buffer
	usock.close()                                           
	for url in parser.urls: print url
