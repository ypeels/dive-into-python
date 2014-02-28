"""Pluralize English nouns (stage 5)

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Command line usage:
$ python plural5.py noun
nouns
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/03/25 15:51:13 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

import re
import string

def buildRule((pattern, search, replace)):
    return lambda word: re.search(pattern, word) and re.sub(search, replace, word)      # combined into 1 function: see 17.7?
                                                                                        # returns a function foo(word) that will execute the lambda when called
def plural(noun, language='en'): 
    lines = file('rules.%s' % language).readlines()                                     # rules offloaded into external data file now
    patterns = map(string.split, lines)                                                 # 17.6: "left as an exercise" to cache the rule file
    rules = map(buildRule, patterns)
    for rule in rules:
        result = rule(noun)                                                             # single call, not if(match): apply
        if result: return result

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print plural(sys.argv[1])
    else:
        print __doc__
