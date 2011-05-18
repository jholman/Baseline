#!/usr/bin/python

# Call me like this:
# pywatch 'python testme.py' *.py


import helper

d = helper.deque('x')

stuff_to_do = '''
None # initialize d
d.push(2)
d.push(4, 0)
d.push(5, 0)
d.pop(1)
d.pop(0)
d.pop(0)
d.pop(0)
d.pop(1)
'''

def indent(text, stop=4):
    return '\n'.join(map(lambda x: ' '*stop + x,str(text).split('\n')))

print '\n','-'*70,'\n'

for line in filter(None,stuff_to_do.split('\n')):
    print "\n%-10s" % line,
    exec('q = ' + line)
    print '     => ' + str(q) if q is not None else ''
    print indent(str(d),0)

