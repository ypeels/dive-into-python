import sys

print 'Dive in'
saveout = sys.stdout                                    # Section 10.2
fsock = open('out.log', 'w')
sys.stdout = fsock
print 'This message will be logged instead of displayed'
sys.stdout = saveout                                    # "Set stdout back to the way it was before you mucked with it. "
fsock.close()
