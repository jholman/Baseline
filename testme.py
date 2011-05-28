#!/usr/bin/python

# Call me like this:
# pywatch 'python testme.py' *.py


import helper


stuff_to_do = '''
d = helper.deque('x')
d.push(2)
d.push(4, 0)
d.push(5, 0)
d.pop(1)
d.pop(0)
d.pop(0)
d.pop(0)
d.pop(1)
s = helper.dstack()
s.push('A')
s.push('B')
s.split(0)
s.push('C')
s.push('D')
s.push('E')
s.split(2)
s.merge()
s.split()
s.pop()
s.pop()
s.merge()

'''

def indent(text, stop=4): return '\n'.join(map(lambda x: ' '*stop + x,str(text).split('\n')))

import time
print '\n', '-'*30, time.ctime(), '-'*30, '\n'

for line in filter(None,stuff_to_do.split('\n')):
    print "\n%-20s" % line,
    exec('q = ' + line)
    print '     =>    ' + str(q) if '=' not in line and q is not None else ''
    print indent(str(eval(line[0])),4)
    
