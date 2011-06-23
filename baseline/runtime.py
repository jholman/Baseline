import sys
from . import helper
from . import stdlib


class BaselineRuntime(object):
    def __init__(self, fundefs=None):
        self.rstack = helper.rstack()
        self.dstack = helper.dstack()
        self.fns = stdlib.stdlib
        if self.fns:
            self.fns.update(fundefs)
        self.pipes = {  0: sys.stdin,
                        1: sys.stdout,
                        2: sys.stderr,
                        }
        self.curr_fn_id = 0
        self.curr_in_idx = 0
        self.uprightness = 1

    def load_defuns(self, L):
        self.fns.update(L)

    def dump_state(self):
        print str(self.dstack)

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
                print "FN  ", inst.val, inst.reg
                self.rstack.append(self.curr_in_idx)            # TODO: not handling inverse mode
                self.rstack.append(self.curr_fn_id)
                self.curr_fn_id, self.uprightness = inst.val, inst.reg
            elif inst.typ is 'literal':
                print "LIT ", inst.val, inst.reg
                self.dstack.append(inst.val, inst.reg)
            pass
        else:
            if type(fn) is type(lambda x:x):
                fn(self, self.uprightness)
            if len(self.rstack) >= 2:
                print "POP "
                self.curr_fn_id = self.rstack.pop()
                self.curr_in_idx = self.rstack.pop()
            else:
                print "QUIT"
                sys.exit(0)

        self.dump_state()       # TODO: delete this line

    def run(self):
        while True:
            self.FDE()


