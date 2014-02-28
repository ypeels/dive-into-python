"""Pluralize English nouns (stage 4)

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Command line usage:
$ python plural4.py noun
nouns
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/03/18 16:43:37 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

import re

def buildMatchAndApplyFunctions((pattern, search, replace)):        # 17.5: builds other functions dynamically. note tuple argument
    matchFunction = lambda word: re.search(pattern, word)           # factored out common function calls
    applyFunction = lambda word: re.sub(search, replace, word)
    return (matchFunction, applyFunction)

patterns = \
  (
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
  )
rules = map(buildMatchAndApplyFunctions, patterns)                  # "rules = buildMatchAndApplyFunctions(patterns)"
# Example 17.11. Unrolling the rules definition
# 
# rules = \
#   (
#     (
#      lambda word: re.search('[sxz]$', word),
#      lambda word: re.sub('$', 'es', word)
#     ),
#     (
#      lambda word: re.search('[^aeioudgkprt]h$', word),
#      lambda word: re.sub('$', 'es', word)
#     ),
#     (
#      lambda word: re.search('[^aeiou]y$', word),
#      lambda word: re.sub('y$', 'ies', word)
#     ),
#     (
#      lambda word: re.search('$', word),
#      lambda word: re.sub('$', 's', word)
#     )
#    )                                          


def plural(noun):                                                   # still unchanged from plural2.py
    for matchesRule, applyRule in rules:
        if matchesRule(noun):
            return applyRule(noun)

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print plural(sys.argv[1])
    else:
        print __doc__
