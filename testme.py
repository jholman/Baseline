#!/usr/bin/python

# Call me like this:
# pywatch 'python testme.py' *.py

import helper

stuff_to_do = '''
d = helper.deque(1)
d.push(2)
d.push(4, 0)
d.push(5, 0)
d.pop()
d.pop(0)
d.pop(0)
d.pop(0)
d.pop(1)
s = helper.dstack()
s.push('ABCDE')
s.split(2)
s.split()
s.merge()
s.pop(1,2)
s.split(1)
s.pop()
s.merge()
s.merge()
s.merge()
'''

def indent(text, stop=4): return '\n'.join(map(lambda x: ' '*stop + x,str(text).split('\n')))

import time
print '\n', '-'*30, time.ctime(), '-'*30, '\n'

for line in filter(None,stuff_to_do.split('\n')):
    print "\n%-20s" % line,
    exec('q = ' + line)
    print '   =' + "%14s" %str(q) if '=' not in line and q is not None else ' '*18,
    rep = str(eval(line[0]))
    print indent(rep,50)[40:]
 
