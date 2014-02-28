"""Convert to and from Roman numerals

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import re

#Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

#Define digit mapping
romanNumeralMap = (('M',  1000),
				   ('CM', 900),
				   ('D',  500),
				   ('CD', 400),
				   ('C',  100),
				   ('XC', 90),
				   ('L',  50),
				   ('XL', 40),
				   ('X',  10),
				   ('IX', 9),
				   ('V',  5),
				   ('IV', 4),
				   ('I',  1))

def toRoman(n):
	"""convert integer to Roman numeral"""
	if not (0 < n < 5000):                                                  # 14.3: "nice Pythonic shortcut". 15.2: upper limit increased from 4000 to meet new "customer requirements"
		raise OutOfRangeError, "number out of range (must be 1..4999)"      # 14.3: optional error message is displayed in traceback if unhandled
	if int(n) <> n:                                                         # 14.3: "<>" same as "!="
		raise NotIntegerError, "non-integers can not be converted"

	result = ""
	for numeral, integer in romanNumeralMap:                                # 14.2: "rich data structure pays off" with simple logic
		while n >= integer:
			result += numeral
			n -= integer
	return result

#Define pattern to detect valid Roman numerals
romanNumeralPattern = re.compile('''                                        # 15.3 (roman81.py): compile regex instead of constantly re-evaluating
	^				   # beginning of string
	M{0,4}			  # thousands - 0 to 4 M's                              # 15.2: increased from 3 to 4 leading M's to meet new "customer requirements"
	(CM|CD|D?C{0,3})	# hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),# 15.3 (roman82.py): {m, n} syntax for a bit of legibility (and speed!)
						#			or 500-800 (D, followed by 0 to 3 C's)
	(XC|XL|L?X{0,3})	# tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
						#		or 50-80 (L, followed by 0 to 3 X's)
	(IX|IV|V?I{0,3})	# ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
						#		or 5-8 (V, followed by 0 to 3 I's)
	$				   # end of string
	''' ,re.VERBOSE)                                                        # 15.3 (roman83.py): verbose regex for legibility

def fromRoman(s):
	"""convert Roman numeral to integer"""
	if not s:                                                               # 15.1: previously-untested corner case
		raise InvalidRomanNumeralError, 'Input can not be blank'
	if not romanNumeralPattern.search(s):                                   # 14.5: with this, all 12 original tests pass!
		raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s

	result = 0
	index = 0
	for numeral, integer in romanNumeralMap:                                # 14.4: same basic loop as toRoman()
		while s[index:index+len(numeral)] == numeral:
			result += integer
			index += len(numeral)
	return result

                                                                            # 15.4: table lookup alternative (not shown here - see roman9.py)