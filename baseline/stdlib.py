
# all functions take a Baseline Runtime as their sole argument

stdlib = {}

## TODO: almost the entire stdlib does insane shit if passed a negative number
###             later observation: I think when I wrote this, I meant the stack_ parts?


def standard(n):
    def stdlibify_helper(f):
        stdlib[n] = f
    return stdlibify_helper

@standard(1)
def stack_pop(blr, reg=1):
    blr.dstack.pop(reg)

@standard(2)
def stack_clone(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(x, reg)
    blr.dstack.append(x, reg)

@standard(3)
def stack_movetobottom(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(x, 1-reg)

@standard(5)
def stack_split(blr, reg=1):
    blr.dstack.split(blr.dstack.pop(reg), reg)

#@standard(6)
#def stack_split_rev(blr, reg=1):
#    blr.dstack.split(blr.dstack.pop(reg), reg, True)

@standard(7)
def stack_merge(blr, reg=1):
    blr.dstack.merge(reg)

@standard(11)
def stack_pop_n(blr, reg=1):
    for i in xrange(blr.dstack.pop(reg)): 
        blr.dstack.pop(reg)

@standard(12)
def stack_clone_n(blr, reg=1):
    l = []
    for i in xrange(blr.dstack.pop(reg)):
        l.append(blr.dstack.pop(reg))
    blr.dstack.extend(l, reg)
    blr.dstack.extend(l, reg)

@standard(13)
def stack_movetobottom_n(blr, reg=1):
    l = []
    for i in xrange(blr.dstack.pop(reg)):
        l.append(blr.dstack.pop(reg))
    blr.dstack.extend(l, 1-reg)

@standard(19)
def stack_debugdump(blr, reg=1):
    blr.dump_state(9)



@standard(21)
def pipes_produce(blr, reg=1):
    fd = blr.dstack.pop(reg)
    n = blr.dstack.pop(reg)

    data = filter(lambda x:x is not None, blr.dstack.pop_n(n, reg))
    data = map(lambda num : chr(int(num % 256)), data)

    if fd in blr.pipes:
        try:
            blr.pipes[fd].write(''.join(data))  # TODO: is there some way to detect partial writes?  what about network sockets?
            blr.pipes[fd].flush()
        except:
            blr.dstack.append(0, reg)           # detects a variety of failures, including closed file
        else:
            blr.dstack.append(n, reg)
    else:
        blr.dstack.append(0, reg)



@standard(30)
def flow_call(blr, reg=1):
    fnid = blr.dstack.pop(reg)
    if fnid is None:
        return
    if not reg:
        fnid *= -1
    blr.rstack.extend([0, fnid])

@standard(31)
def flow_call_if(blr, reg=1):
    flag = blr.dstack.pop(reg)
    if flag:
        stdlib[30](blr, reg)
    else:
        blr.dstack.pop(reg)

@standard(32)
def flow_call_ifelse(blr, reg=1):
    flag = blr.dstack.pop(reg)
    iffalse, iftrue = blr.dstack.pop_n(2, reg)
    if flag:
        blr.dstack.append(iftrue, reg)
    else:
        blr.dstack.append(iffalse, reg)
    stdlib[30](blr, reg)

def make_n_ary_fn(fid, n, fn):
    def f(blr, reg=1):
        args = reversed(blr.dstack.pop_n(n, reg))
        blr.dstack.append(fn (*args), reg)
    stdlib[fid] = f

import operator, math
for fid, n, fn in [ [ 50, 2, operator.add],
                    [ 51, 2, operator.sub],
                    [ 52, 2, operator.mul],
                    [ 53, 2, operator.floordiv],
                    [ 54, 2, operator.mod],
                    [ 55, 2, operator.pow],
                    [ 56, 2, math.log],
                    [ 57, 2, operator.truediv],
                    [ 60, 1, operator.not_],
                    [ 61, 2, operator.iand],
                    [ 62, 2, operator.ior],
                    [ 63, 2, operator.ixor],
                    #[ 70, 1, lambda x: ~x],
                    [ 71, 2, operator.and_],
                    [ 72, 2, operator.or_],
                    [ 73, 2, operator.xor],
                    [ 74, 2, operator.lshift],
                    [ 75, 2, operator.rshift],
                    [ 80, 2, operator.lt],
                    [ 81, 2, operator.le],
                    [ 82, 2, operator.eq],
                    [ 83, 2, operator.ge],
                    [ 84, 2, operator.gt],
                    [ 85, 2, operator.ne],
                    ]:
    make_n_ary_fn(fid, n, fn)






# Is this sillines really called for?
ll = locals()
for l in dict(locals()):
    if not l.startswith('__') and l not in ["stdlib", "ll"]:
        del ll[l]
del ll

