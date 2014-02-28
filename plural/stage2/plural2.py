"""Pluralize English nouns (stage 2)

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Command line usage:
$ python plural2.py noun
nouns
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2004/03/18 18:55:45 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

import re

def match_sxz(noun):
    return re.search('[sxz]$', noun)

def apply_sxz(noun):
    return re.sub('$', 'es', noun)

def match_h(noun):
    return re.search('[^aeioudgkprt]h$', noun)

def apply_h(noun):
    return re.sub('$', 'es', noun)

def match_y(noun):
    return re.search('[^aeiou]y$', noun)
        
def apply_y(noun):
    return re.sub('y$', 'ies', noun)

def match_default(moun):
    return 1

def apply_default(noun):
    return noun + 's'

rules = ((match_sxz, apply_sxz),                    # lookup table for rules (not a dictionary [which is unordered], because rules have an order of precedence)
         (match_h, apply_h),
         (match_y, apply_y),
         (match_default, apply_default)
         )

def plural(noun):
    for matchesRule, applyRule in rules:
        if matchesRule(noun):
            return applyRule(noun)
            
# 17.3: "unrolling the function"
# def plural(noun):
#     if match_sxz(noun):
#         return apply_sxz(noun)
#     if match_h(noun):
#         return apply_h(noun)
#     if match_y(noun):
#         return apply_y(noun)
#     if match_default(noun):
#         return apply_default(noun)

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print plural(sys.argv[1])
    else:
        print __doc__
