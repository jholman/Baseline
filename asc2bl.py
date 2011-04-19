#!/usr/bin/python
# -*- coding=utf-8 -*-

import getopt
import string
import sys
#from baseline import _basechars, _subchars, _superchars

_basechars  = u"0123456789+-=()<>^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_subchars   = u"₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳ₐ   ₑ   ᵢ     ₒ  ᵣ  ᵤᵥ ₓ                            "
_superchars = u"⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ ʳˢᵗᵘᵛʷˣʸᶻᴬᴮ ᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ   "


_triples = zip(_basechars,_subchars,_superchars)
_goodkeys = [a for a,b,c in _triples if b!=' ' and c!=' ']
_base2sup = dict(z for z in zip(_basechars,_superchars) if z[1]!=' ' and z[0] in _goodkeys)
_base2sub = dict(z for z in zip(_basechars,_subchars) if z[1]!=' ' and z[0] in _goodkeys)
_sup2base = dict(z for z in zip(_superchars,_basechars) if z[0]!=' ' and z[1] in _goodkeys)
_sub2base = dict(z for z in zip(_subchars,_basechars) if z[0]!=' ' and z[1] in _goodkeys)
_base2base= dict(zip(_basechars,_basechars))

def asc2bl_1(line, state='-', linenum=-1):
    if ':=' not in line:
        return line
    ans = ''
    inquote = False
    for ci,c in enumerate(line):
        if not inquote:
            if c in '-AV':
                state = c
            elif state in 'AV' and c in '\'"':
                inquote = c
            elif state=='-' or c in string.whitespace:
                ans += c
            elif c in _goodkeys:
                if state=='A':
                    ans += _base2sup[c]
                else: # state == 'V'
                    ans += _base2sub[c]
            else:
                raise Exception("bullshit character at line %d, column %d: %s\n%s\n%s" % (linenum+1,ci+1,c,line,' '*ci + '^'))
        else:
            if c is inquote[0]:
                inquote2 = map(ord,inquote[1:]) + [len(inquote[1:])]
                inquote3 = '(' + " ".join(map(str,inquote2)) + ')'
                ans += asc2bl_1(inquote3,state)
                inquote = False
            else:
                inquote += c
    return ans

def bl2asc_1(line):
    line = unicode(line,'utf-8')
    ans = ''
    state = '-'
    dicts = {'-':_base2base, 'A':_sup2base, 'V':_sub2base}
    for c in line:
        if c in string.whitespace:
            ans += c
        elif c in _sub2base.keys():
            if state != 'V':
                ans += 'V'
                state = 'V'
            ans += _sub2base[c]
        elif c in _sup2base.keys():
            if state != 'A':
                ans += 'A'
                state = 'A'
            ans += _sup2base[c]
        elif c in '-AV':
            raise Exception("bullshit!")
        else:
            if state != '-':
                ans += '-'
                state = '-'
            ans += c

#        elif c in dicts[state].keys():
#            ans += dicts[state][c]
#        else:
#            found = False
#            for s in dicts.keys():
#                if c in dicts[s].keys():
#                    state = s
#                    ans += s + dicts[state][c]
#                    found = True
#                    break
#            if not found:
#                raise Exception("in state %s, this character is bullshit: %s" % (state,c))
    return ans
        

def asc2bl(lines):
    return [asc2bl_1(string.rstrip(line), linenum=li) for li,line in enumerate(lines)]

def bl2asc(lines):
    return [bl2asc_1(string.rstrip(line)) for line in lines]



def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
        print >>sys.stderr, msg
        print >>sys.stderr, "for help use --help"
        return 2

    if argv[0].endswith('bl2asc'):
        #print "selecting bl2asc"
        converter = bl2asc
    else:
        #print "selecting asc2bl"
        converter = asc2bl

    try:
        filename = args[0]
    except:
        filename = None
            
    if filename is None:
        ans = converter(sys.stdin)
    else:
        with file(filename) as f:
            ans = converter(f)

    if len(ans) > 0 and ans[-1] == '\n':        # wtf is this necessary?
        print "aha"
        ans = ans[:-1]


    ans2 = u'\n'.join(ans).encode('utf-8')
    print ans2
    
    #####
    #
    # CODE GOES HERE
    #
    #####


if __name__ == "__main__":
    sys.exit(main())
