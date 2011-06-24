
# all functions take a Baseline Runtime as their sole argument

stdlib = {}

## TODO: almost the entire stdlib does insane shit if passed a negative number


def standard(n):
    def stdlibify_helper(f):
        stdlib[n] = f
        return f
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



@standard(50)
def stack_plus(blr, reg=1):
    blr.dstack.append(blr.dstack.pop(reg) + blr.dstack.pop(reg), reg)

@standard(51)
def stack_minus(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(blr.dstack.pop(reg) - x)

@standard(52)
def stack_times(blr, reg=1):
    blr.dstack.append(blr.dstack.pop(reg) * blr.dstack.pop(reg), reg)

@standard(53)
def stack_div(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(blr.dstack.pop(reg) / x)

@standard(54)
def stack_div(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(blr.dstack.pop(reg) % x)

@standard(55)
def stack_div(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(blr.dstack.pop(reg) ** x)

@standard(56)
def stack_div(blr, reg=1):
    from math import log
    x = blr.dstack.pop(reg)
    blr.dstack.append(log(blr.dstack.pop(reg), x))




@standard(21)
def pipes_produce(blr, reg=1):
    fd = blr.dstack.pop(reg)
    n = blr.dstack.pop(reg)
    data = []
    for i in range(n):
        data.append(chr(blr.dstack.pop(reg)))
    data = filter(lambda x:x is not None, data)
    if fd in blr.pipes:
        # TODO: should probably check for closed-ness here?
        blr.pipes[fd].write(''.join(data))
        # TODO: should do something to ensure writing worked?  oh well, just go for it.
        blr.pipes[fd].flush()
        blr.dstack.append(n, reg)
    else:
        blr.dstack.append(reg)
