"""Regression testing framework

This module will search for scripts in the same directory named
XYZtest.py.  Each such script should be a test suite that tests a
module through PyUnit.  (As of Python 2.1, PyUnit is included in
the standard library as 'unittest'.)  This script will aggregate all
found test suites into one big test suite and run them all at once.

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2004/05/05 21:57:19 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import sys, os, re, unittest

def regressionTest():
    path = os.path.abspath(os.path.dirname(sys.argv[0]))        # 16.2: full absolute path of regression.py's directory
    files = os.listdir(path)                                    # 16.3: "ls $path"
    test = re.compile("test\.py$", re.IGNORECASE)               # what's with the backslash??
    files = filter(test.search, files)                          # 16.3: filter for all files ending in "test.py". historical note: map()/filter() predate list comprehensions (introduced in Python 2.0)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]     # 16.4: splitext() = (name, extension)
    moduleNames = map(filenameToModuleName, files)              # - apply splitext()[0] to all filtered files
    modules = map(__import__, moduleNames)                      # 16.6: dynamic imports!
    load = unittest.defaultTestLoader.loadTestsFromModule       # 16.7: introspect to determine classes/functions
    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    unittest.main(defaultTest="regressionTest")                 # overrides unittest's usual magic
