import sys

fsock = open('error.log', 'w')
sys.stderr = fsock                              # Section 10.2
print 'print >> std.stderr prints to stderr; same syntax for any file-like object' >> std.stderr
raise Exception, 'this error will be logged'

# the following text gets logged:
# Traceback (most recent call last):
#   File "stderr.py", line 5, in <module>
#     raise Exception, 'this error will be logged'
# Exception: this error will be logged

print 'this line never gets printed, due to the unhandled Exception'