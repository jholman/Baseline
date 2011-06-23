import sys
from baseline import helper


class BaselineRuntime(object):
    def __init__(self, fundefs=None):
        self.rstack = helper.rstack()
        self.dstack = helper.dstack()
        self.fns = fundefs or {}
        self.pipes = {  0: sys.stdin,
                        1: sys.stdout,
                        2: sys.stderr,
                        }
        self.curr_fn_id = 0
        self.curr_in_idx = 0

    def load_defuns(self, L):
        self.fns.update(L)

    def dump_state(self):
        print str(self.dstack)

    def FDE(self):
        #fetch
        thisfun = this.fns.get(self.curr_fn_id, None)
        if thisfun is None:
            raise Exception("Attempted to execute code for invalid function #%d" % self.curr_fn_id)
        if self.curr_in_idx < len(thisfun):
            # do it
            pass
        else:
            # pop
            pass

    def run(self):
        while True:
            self.FDE()

