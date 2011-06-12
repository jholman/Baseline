# -*- coding=utf-8 -*-

#from baseline import _basechars
from . import _basechars, _subchars, _superchars, _sub2base, _super2base
import re
from pprint import pprint



__registers = _subchars, _superchars
__subdigits = _subchars[:10]
__superdigits = _superchars[:10]
operator_bases = "+-=<>^_"
operator_indices = [_basechars.index(c) for c in operator_bases]
operators = ''.join(r[i] for r in __registers for i in operator_indices)
parens = [r[_basechars.index(baseparen)] for r in __registers for baseparen in "()"]


# TODO: this function is an inelegant mess
def classify_token(string):
    if len(string) == 0:
        return ("comment", None, None)

    tokentypemap = {"number"    : __subdigits + __superdigits,
                    "operator"  : operators,
                    "paren"     : parens,
                    }
    tokentype = "comment"
    for name, group in tokentypemap.items():
        if string[0] in group:
            tokentype = name

    register = None
    conversion = lambda x:x
    if string[0] == " ":
        pass
    elif string[0] in _superchars:
        register = "up"
        conversion = _super2base.get
    elif string[0] in _subchars:
        register = "down"
        conversion = _sub2base.get

    value = ''.join(conversion(l) for l in string)
    if tokentype == "number":
        value = int(value,0)

    return (tokentype, register, value)


def tokenize_line(line):
    pattern = "[%s]+|[%s]+|[%s]|" % (__subdigits, __superdigits, operators)
    pattern += "|".join("%s+"%p for p in parens)

    tokens = filter(lambda s: len(s)>0,re.split("(%s)" % pattern,line))

    richtokens = []
    offset = 0
    for t in tokens:
        richtokens.append(tuple((classify_token(t), t, (offset,))))
        offset += len(t)
                    
    return richtokens


