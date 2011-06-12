# -*- coding=utf-8 -*-

from . import _super2base, _sub2base, _subchars, _superchars
import helper

#from baseline import _basechars, _subchars, _superchars

#_basechars  = u"0123456789+-=()<>^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#_subchars   = u"₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳ₐ   ₑ   ᵢ     ₒ  ᵣ  ᵤᵥ ₓ                            "
#_superchars = u"⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ ʳˢᵗᵘᵛʷˣʸᶻᴬᴮ ᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ   "

def _intify(intstr):
    '''Converts base-10, base-16, and base-2 strings to integers.

    Deliberately ignores base-8, because I hate base-8.  If I ever stop
    hating base-8, replace this whole function with a call to int(intstr,0)

    >>> map(_intify,['1','02','0x03','011','0x11','0b11'])
    [1, 2, 3, 11, 17, 3]
    '''

    if intstr.startswith('0x'):
        return int(intstr,16)
    elif intstr.startswith('0b'):
        return int(intstr,2)
    else:
        return int(intstr,10)


def parseline(line):
    '''Compiles a single line of baseline into bytecode.

    Takes a string of the form
        INT := stuff
    or any freeform string containing no colon-equals digraph (comment).

    If the colon-equals is present, returns a triple (word,list,line), where
    list contains a list of (register,item) pairs.  Register is one of 'AV';
    each item is an integer (comments do not make it into the list).

    If the entire line is a comment, the return value is (None, [], line)

    In either case, the third element of the returned triple is the input line,
    for debugging.

    Wow, doctests don't work on unicode.  WTF python!

    >>> parseline(u'99 := \u2088\u2088eight ')
    (99, [('V', 88)], u'99 := \u2088\u2088eight ')

    >>> parseline(u'100 := \u2077\u2078 \u2077\u2078\u2084\u2085\u2077\u207866\u2084\u2085 \u2084 \u2085 \u2084\u2085Hilarious')
    (100, [('A', 78), ('A', 78), ('V', 45), ('A', 78), ('V', 45), ('V', 4), ('V', 5), ('V', 45)], u'100 := \u2077\u2078 \u2077\u2078\u2084\u2085\u2077\u207866\u2084\u2085 \u2084 \u2085 \u2084\u2085Hilarious')'''

    wordname, sep, rest = line.partition(':=')
    if sep != u':=':
        return (None, [], line)

    wordname = _intify(wordname.strip())    # deliberately allowing exception to bubble up

    register = '-'
    cc = ''
    wordlist = []
    for ci,c in enumerate(rest.strip()):
        if c == ' ':
            newregister = '-'
        elif c in _subchars:
            newregister = 'V'
        elif c in _superchars:
            newregister = 'A'
        else:
            newregister = '-'
        #print c, repr(c), type(c), newregister
        if register not in ['-', newregister] and cc != '':
            #print "appending '%s'" % cc
            d = _sub2base if register == 'V' else _super2base
            newword = _intify(''.join(map(d.get,cc)))
            wordlist.append((register,newword))
            cc = ''
        if newregister != '-':
            cc += c
        #else: cc = ''
        register = newregister
    return (wordname,wordlist,line)



class BaselineEnv(object):
    def __init__(self):
        self.rstack = helper.rstack()
        self.dstack = helper.dstack()
        self.fns = {}
        self.pipes = {  0: sys.stdin,
                        1: sys.stdout,
                        2: sys.stderr,
                        }


