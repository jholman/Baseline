# -*- coding=utf-8 -*-

_basechars  = u"0123456789+-=()<>^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_subchars   = u"₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎˱˲˰˯˳ₐ   ₑ   ᵢ     ₒ  ᵣ  ᵤᵥ ₓ                            "
_superchars = u"⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾˂˃˄˅˚ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ ʳˢᵗᵘᵛʷˣʸᶻᴬᴮ ᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ   "

_triples = zip(_basechars,_subchars,_superchars)
_goodkeys = [a for a,b,c in _triples if b!=' ' and c!=' ']
_base2super = dict(z for z in zip(_basechars,_superchars) if z[0] in _goodkeys)
_base2sub   = dict(z for z in zip(_basechars,_subchars)   if z[0] in _goodkeys)
_super2base = dict(z for z in zip(_superchars,_basechars) if z[1] in _goodkeys)
_sub2base   = dict(z for z in zip(_subchars,_basechars)   if z[1] in _goodkeys)
_base2base  = dict(zip(_basechars,_basechars))

