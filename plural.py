"""Pluralize English nouns (stage 6)

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Command line usage:
$ python plural6.py noun
nouns
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"   # essentially same code as plural6.py
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/05/03 19:40:42 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

import re

def rules(language):                                    # 17.7: "yield" means this is a generator ("resumable function") - it spits out rule(word) functions.
    for line in file('plural-rules.%s' % language):     # idiom for reading one line at a time from a file. also generator-based!
        pattern, search, replace = line.split()         # parse plural-rules.en from known format
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)   # return a closure (uses local variables pattern, search, replace as constants)
                                                        # - re.sub() performs regex-based string substitutions
def plural(noun, language='en'):                        # 17.2: plural1.py previously used inline regexes, then gradually evolved into this
    """returns the plural form of a noun"""
    for applyRule in rules(language):                   # 17.7: for loop will create generator object "rules(language)" AND successively calls its next() method
        result = applyRule(noun)                            # advantage over plural5.py: construct rule functions lazily    
        if result: return result

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print plural(sys.argv[1])
    else:
        print __doc__
