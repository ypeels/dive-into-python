print '''
This is awesome!!!
You have to add "re.VERBOSE" as an extra argument to re.search() or re.compile()
but that lets you use a "verbose" regex in which whitespace AND COMMENTS are ignored!!!

Below is Example 7.9.
'''

import re
pattern = '''
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
'''
print re.search(pattern, 'M', re.VERBOSE)
print re.search(pattern, 'MCMLXXXIX', re.VERBOSE)
print re.search(pattern, 'MMMMDCCCLXXXVIII', re.VERBOSE)
print re.search(pattern, 'M')   # None [didn't specify re.VERBOSE!] 
