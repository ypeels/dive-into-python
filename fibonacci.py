"""Fibonacci sequences using generators

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

def fibonacci(max):                                     # 17.7 Example 17.19: Using generators instead of recursion
    a, b = 0, 1
    while a < max:
        yield a                                         # 17.7: "you could do [this] with recursion, but this way is easier to read"
        a, b = b, a+b

for n in fibonacci(1000):                               # for loop creates generator object AND successively calls its next() method
    print n,                                        
