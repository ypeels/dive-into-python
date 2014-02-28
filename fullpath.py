import sys, os                                  # Section 16.2: Finding the path

print 'sys.argv[0] =', sys.argv[0]
pathname = os.path.dirname(sys.argv[0])
print 'path =', pathname                        # directory portion (may be blank)
print 'full path =', os.path.abspath(pathname)  # abspath('') == current working directory == os.getcwd(). "normalized" (relative paths are made absolute and as simple as possible)
                                                # n.b. path NEED NOT EXIST - this is just string manipulation