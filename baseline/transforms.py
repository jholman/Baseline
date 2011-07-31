# -*- coding=utf-8 -*-


from . import _basechars, _subchars, _superchars, _sub2base, _super2base
import re
from pprint import pprint

__registers = _subchars, _superchars
__subdigits = _subchars[:10]
__superdigits = _superchars[:10]
operator_indices = [_basechars.index(c) for c in "+-=<>^_"]
operators = ''.join(r[i] for r in __registers for i in operator_indices)
parens = [r[_basechars.index(baseparen)] for r in __registers for baseparen in "()"]

class richtoken(object):
    def __init__(self, typ, reg, val, t, loc=(0,)):
        self.typ, self.reg, self.val, self.tok, self.loc = typ, reg, val, t, loc
    def __repr__(self):
        return "richtoken(%s, %s, %s, %s, %s)" % tuple(map(repr, [self.typ, self.reg, self.val, self.tok, self.loc]))
    def __eq__(self, other):
        return issubclass(other.__class__, self.__class__) and self.__dict__ == other.__dict__


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
        register = 1
        conversion = _super2base.get
    elif string[0] in _subchars:
        register = 0
        conversion = _sub2base.get

    value = ''.join(conversion(l) for l in string)
    if tokentype == "number":
        value = int(value, 0)

    return (tokentype, register, value)


def tokenize_line(line):
    # token output format:  richtoken(type, register, value, token, location)
    line = line.split("#")[0]       # '#' marks comments to end-of-line
    pattern = "[%s]+|[%s]+|[%s]|" % (__subdigits, __superdigits, operators)
    pattern += "|".join("%s+"%p for p in parens)

    tokens = filter(lambda s: len(s)>0, re.split("(%s)" % pattern, line))

    newtokens = []
    offset = 0
    for t in tokens:
        typ, reg, val = classify_token(t)
        newtokens.append(richtoken(typ, reg, val, t, (offset,)))
        offset += len(t)
                    
    return newtokens


def parse_fundef(line):
    # TODO: fix up all the stupid parse exceptions, so that they do something useful with all that tok/loc I'm passing around
    tokens = filter(lambda x: x.typ != "comment", tokenize_line(line))

    if len(tokens) == 0:
        return None
    if len(tokens) < 3:
        raise ValueError("you need more than a couple of tokens to make a function definition")
    if tokens[0].typ != 'number' or not tokens[0].reg:
        raise ValueError("fundefs must start with a number in a register")
    if tokens[1].val != u'='     or not tokens[1].reg:
        raise ValueError("fundefs must use = to assign operations to a function-id")

    function_id = tokens[0]
    assign_op = tokens[1]
    tokens = tokens[2:]

    # At this point, `tokens` is the function body, and has at least one element
    # Now we enter a tediously hand-coded State Machine
    newtokens = []
    state = 'plain'
    counter, state_reg, state_num = None, None, None
    while len(tokens):
        head = tokens.pop(0)
        if state == 'plain':
            if head.typ == 'number':
                newtokens.append(richtoken('fncall', head.reg, head.val, head.tok, head.loc))
            elif head.typ == 'paren':
                if len(head.val) not in [1, 2]:
                    raise Exception("SYNTAX ERROR OMG, what the hell is this mass of parens?")     # TODO: something useful
                if head.val not in ["(", "(("]:
                    raise Exception("SYNTAX ERROR OMG, why am I seeing a close-paren right now?")     # TODO: something useful
                state = 'literal'
                counter = 0
                state_reg = head.reg
                state_num = len(head.val)
            else:
                raise NotImplementedError("operators are not currently well-defined inside function bodies")
        elif state == 'literal':
            if head.typ == 'number':
                if head.reg == state_reg:
                    newtokens.append(richtoken('literal', head.reg, head.val, head.tok, head.loc))
                    counter += 1
                else:
                    raise Exception("SYNTAX ERROR OMG, why can't you stay in the register of the parens?!?")    # TODO: something useful
            elif head.typ == 'paren':
                if state_reg == head.reg and len(head.val) == state_num:
                    if state_num == 2:
                        newtokens.append(richtoken('literal', head.reg, counter, head.tok, head.loc))
                    state = 'plain'
                else:
                    raise Exception("SYNTAX ERROR OMG, you've gotta close the parens you opened")     # TODO: something useful
            else:
                raise NotImplementedError("operators are not currently well-defined inside function bodies")
        else:
            raise Exception("parser's state machine went haywire")

    if function_id.reg == 0:
        # TODO: invert all registers if function_id.reg is 'down'
        pass
    return function_id.val, newtokens

