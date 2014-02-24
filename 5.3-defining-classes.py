class Base: 
    def __init__(self):
        print "Base.__init__()"

class Derived(Base):
    pass
    
# 5.3.2: "__init__ methods are optional, but when you define one, you must remember to explicitly call the ancestor's __init__ method"
# Q: but what if you DON'T define one? will Base.__init__() be called??

d = Derived()
# A: yes, Base.__init__() is still called.
#   - i think this just reflects the fact that Derived.__init__() would be an OVERRIDE
    