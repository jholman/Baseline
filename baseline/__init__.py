# -*- coding=utf-8 -*-

import sys
import argparse

_basechars  = u"0123456789+-=()<>^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_subchars   = u"₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳ₐ   ₑ   ᵢ     ₒ  ᵣ  ᵤᵥ ₓ                            "
_superchars = u"⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ ʳˢᵗᵘᵛʷˣʸᶻᴬᴮ ᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ   "

__triples = zip(_basechars,_subchars,_superchars)
__goodkeys = [a for a,b,c in __triples if b!=' ' and c!=' ']
_base2super = dict(z for z in zip(_basechars,_superchars) if z[0] in __goodkeys)
_base2sub   = dict(z for z in zip(_basechars,_subchars)   if z[0] in __goodkeys)
_super2base = dict(z for z in zip(_superchars,_basechars) if z[1] in __goodkeys)
_sub2base   = dict(z for z in zip(_subchars,_basechars)   if z[1] in __goodkeys)
_base2base  = dict(zip(_basechars,_basechars))

del a, b, c, __triples, __goodkeys


# If these are earlier in the file than the constant-definitions 
#   (e.g. _basechars), then infinite recursirve import causes a crash.
# Probably that means I'm doing something stylistically stupid.
from .runtime import BaselineRuntime
from .transforms import parse_fundef


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args(argv)

    
    # TODO: the "unicode(l, 'utf-8')" in the next line is only poorly understood,
    #   and really should be replaced with something more intelligent

    fns = dict(filter(None, (parse_fundef(unicode(l, 'utf-8')) for l in args.infile)))
    from pprint import pprint
    pprint(fns)

    env = BaselineRuntime(fundefs = fns)

