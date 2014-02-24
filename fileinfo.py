"""Framework for getting filetype-specific metadata.

Instantiate appropriate class with filename.  Returned object acts like a
dictionary, with key-value pairs for each piece of metadata.
    import fileinfo
    info = fileinfo.MP3FileInfo("/music/ap/mahadeva.mp3")
    print "\\n".join(["%s=%s" % (k, v) for k, v in info.items()])

Or use listDirectory function to get info on all files in a directory.
    for info in fileinfo.listDirectory("/music/ap/", [".mp3"]):
        ...

Framework can be extended by adding classes for particular file types, e.g.
HTMLFileInfo, MPGFileInfo, DOCFileInfo.  Each class is completely responsible for
parsing its files appropriately; see MP3FileInfo for example.

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import os
import sys
from UserDict import UserDict                           # 5.2: imports UserDict.UserDict, but NOT UserDict itself!

def stripnulls(data):
    "strip whitespace and nulls"
    return data.replace("\00", " ").strip()

class FileInfo(UserDict):                               # 5.5: before Python 2.2, you couldn't inherit from built-in types - you had to use UserList, UserDict, etc. instead
    "store file metadata"
    def __init__(self, filename=None):
        UserDict.__init__(self)                         # 5.3: calling base-class "constructor" (must be done explicitly)
        self["name"] = filename
    
class MP3FileInfo(FileInfo):
    "store ID3v1.0 MP3 tags"
    tagDataMap = {"title"   : (  3,  33, stripnulls),
                  "artist"  : ( 33,  63, stripnulls),
                  "album"   : ( 63,  93, stripnulls),
                  "year"    : ( 93,  97, stripnulls),
                  "comment" : ( 97, 126, stripnulls),
                  "genre"   : (127, 128, ord)}
    
    def __parse(self, filename):
        "parse ID3v1.0 tags from MP3 file"
        self.clear()
        try:
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()                           # 6.2: multiple calls to close() will fail silently.
            if tagdata[:3] == 'TAG':
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    self[tag] = parseFunc(tagdata[start:end])
        except IOError:
            pass

    def __setitem__(self, key, item):                   # 5.6: called when you use dict-like [] to write? Python's signature (called via "base class code")
        if key == "name" and item:                          # see also 5.7 for __repr__, __cmp__, __len__, __delitem__
            self.__parse(item)                              # basically operator overloading, but with "secret" function names
        FileInfo.__setitem__(self, key, item)

def listDirectory(directory, fileExtList):
    "get list of file info objects for files of particular extensions"
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):    # 6.4: scan FileInfo's module for class %sFileInfo
        "get file info class from filename extension"
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]     # 6.6: "1:" slices off the dot before the extension
        return hasattr(module, subclass) and getattr(module, subclass) or FileInfo  # 6.4: “If this module has the class named by subclass then return it, otherwise return the base class FileInfo [NOT a class instance].” 
    return [getFileInfoClass(f)(f) for f in fileList]                           # 6.6: FileInfo.__init__() triggers subclass's __setitem__                  

if __name__ == "__main__":
    for info in listDirectory("/music/_singles/", [".mp3"]):
        print "\n".join(["%s=%s" % (k, v) for k, v in info.items()])
        print
