'''OpenAnything: a kind and thoughtful library for HTTP web services

This program is part of 'Dive Into Python', a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
'''

__author__ = 'Mark Pilgrim (mark@diveintopython.org)'
__version__ = '$Revision: 1.6 $'[11:-2]
__date__ = '$Date: 2004/04/16 21:16:24 $'
__copyright__ = 'Copyright (c) 2004 Mark Pilgrim'
__license__ = 'Python'

import urllib2, urlparse, gzip
from StringIO import StringIO

USER_AGENT = 'OpenAnything/%s +http://diveintopython.org/http_web_services/' % __version__

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):                        # 11.7: Handling redirects - Example 11.11
    def http_error_301(self, req, fp, code, msg, headers):                      # permanent redirect (update your address book!)
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code                                                    # also store status code, which base class does not, for some reason
        return result

    def http_error_302(self, req, fp, code, msg, headers):                      # temporary redirect (should not update your address book)
        result = urllib2.HTTPRedirectHandler.http_error_302(                        # would it have been cleaner to merge into http_error_redirect()?
            self, req, fp, code, msg, headers)                                      # or maybe use *args?
        result.status = code
        return result

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):                     # Section 11.6 Example 11.7
    def http_error_default(self, req, fp, code, msg, headers):                  # python docs: base class turns all responses into HTTPError exceptions
        result = urllib2.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result                                                           # subclass RETURNS the exception instead of raising
                                                                                    # would it have been cleaner to call base class's method and CATCH the exception?
def openAnything(source, etag=None, lastmodified=None, agent=USER_AGENT):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    If the etag argument is supplied, it will be used as the value of an
    If-None-Match request header.

    If the lastmodified argument is supplied, it must be a formatted
    date/time string in GMT (as returned in the Last-Modified header of
    a previous request).  The formatted date/time will be used
    as the value of an If-Modified-Since request header.

    If the agent argument is supplied, it will be used as the value of a
    User-Agent request header.
    """

    if hasattr(source, 'read'):
        return source

    if source == '-':
        return sys.stdin

    if urlparse.urlparse(source)[0] == 'http':                                          # 11.9: make sure you're dealing with an HTTP URL
        # open URL with urllib2
        request = urllib2.Request(source)                                               # 11.5 Example 11.4: first, create a Request object
        request.add_header('User-Agent', agent)                                         # 11.5: Setting the User-Agent
        if lastmodified:                                                                    # trivium: HTTP header field names are case-insensitive
            request.add_header('If-Modified-Since', lastmodified)                       # 11.6: if data hasn't changed, server should return 304, which raises HTTPError exception
        if etag:
            request.add_header('If-None-Match', etag)                                   # 11.6: request page hash (serves same purpose as LastModified)    
        request.add_header('Accept-encoding', 'gzip')                                   # 11.8: Servers won't give you compressed data unless you tell them you can handle it.
        opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())    # second, create a URL opener. (11.6: this allows you to specify a custom error-handler easily [11.9: in order of decreasing priority])
        return opener.open(request)                                                     # finally, use opener to open the Request
    
    # try to open with native open function (if source is a filename)
    try:
        return open(source)
    except (IOError, OSError):
        pass

    # treat source as string
    return StringIO(str(source))

def fetch(source, etag=None, lastmodified=None, agent=USER_AGENT):                      # 11.9: Putting it all together
    '''Fetch data and metadata from a URL, file, stream, or string'''
    result = {}
    f = openAnything(source, etag, lastmodified, agent)
    result['data'] = f.read()
    if hasattr(f, 'headers'):                                                           # 11.9: store headers for future invocations
        # save ETag, if the server sent one
        result['etag'] = f.headers.get('ETag')
        # save Last-Modified header, if the server sent one
        result['lastmodified'] = f.headers.get('Last-Modified')
        if f.headers.get('content-encoding') == 'gzip':                                 # 11.8: Handling compressed data
            # data came back gzip-compressed, decompress it
            result['data'] = gzip.GzipFile(fileobj=StringIO(result['data'])).read()     # workaround: "write" gzipped data to "string-file" in memory, since GzipFile requires a file-like object
    if hasattr(f, 'url'):                                                                   # Example 11.6: gzip cannot unzip f directly from server, due to implementation constraints
        result['url'] = f.url
        result['status'] = 200                                                          # 11.9: default status is OK
    if hasattr(f, 'status'):
        result['status'] = f.status                                                     # from DefaultErrorHandler()
    f.close()