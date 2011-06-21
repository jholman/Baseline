# -*- coding=utf-8 -*-

import argparse
#import baseline.runtime.BaselineRuntime

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




def main(argv):
    import baseline
    print baseline
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))

    #env = baseline.runtime.BaselineRuntime

