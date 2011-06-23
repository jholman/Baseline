import sys
from . import helper
from . import stdlib


def _reg_merge(x, y):
    #return y
    assert x in [0,1] and y in [0,1]
    return 1 if x==y else 0


class BaselineRuntime(object):
    def __init__(self, fundefs=None, debug=0):
        self.rstack = helper.rstack()
        self.dstack = helper.dstack()
        self.fns = dict(stdlib.stdlib)
        if self.fns:
            self.fns.update(fundefs)
        self.pipes = {  0: sys.stdin,
                        1: sys.stdout,
                        2: sys.stderr,
                        }
        self.curr_fn_id = 0
        self.curr_in_idx = 0
        self.uprightness = 1
        self.debuglevel = debug

    def load_defuns(self, L):
        self.fns.update(L)

    def dump_state(self):
        if self.debuglevel > 5:
            print str(self.dstack)
            print str(self.rstack)
            print (self.curr_fn_id, self.curr_in_idx, self.uprightness)

    def FDE(self):
        # this is the fetch
        fn = self.fns.get(self.curr_fn_id, None)
        if fn is None:
            raise Exception("Attempted to execute code for invalid function #%d" % self.curr_fn_id)

        # and the rest is decode/execute, all intermingled
        if type(fn) is not type(lambda x:x) and self.curr_in_idx < len(fn):
            inst = fn[self.curr_in_idx]
            self.curr_in_idx += 1
            if inst.typ is 'fncall':
                if self.debuglevel > 5: print "FN  ", inst.val, inst.reg
                self.rstack.append(self.curr_in_idx)
                self.rstack.append(self.curr_fn_id * (1 - (2 * self.uprightness)))
                self.curr_fn_id = inst.val
                self.uprightness = _reg_merge(self.uprightness, inst.reg)
                self.curr_in_idx = 0
            elif inst.typ is 'literal':
                if self.debuglevel > 5: print "LIT ", inst.val, inst.reg
                self.dstack.append(inst.val, _reg_merge(self.uprightness, inst.reg))
            pass
        else:
            if type(fn) is type(lambda x:x):
                fn(self, self.uprightness)
            if len(self.rstack) >= 2:
                if self.debuglevel > 5: print "POP "
                self.curr_fn_id = self.rstack.pop()
                self.uprightness = 1
                if self.curr_fn_id < 0:
                    self.uprightness = 0
                    self.curr_fn_id *= -1
                self.curr_in_idx = self.rstack.pop()
            else:
                if self.debuglevel > 5: print "QUIT"
                sys.exit(0)

        self.dump_state()       # TODO: delete this line

    def run(self):
        while True:
            self.FDE()


