
# all functions take a Baseline Runtime as their sole argument

stdlib = {}


# TODO: omg, write a decorater to insert functions into the stdlib

def stack_pop(blr, reg=1):
    blr.dstack.pop(reg)

stdlib[1] = stack_pop

def stack_clone(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(x, reg)
    blr.dstack.append(x, reg)
stdlib[2] = stack_clone

def stack_movetobottom(blr, reg=1):
    x = blr.dstack.pop(reg)
    blr.dstack.append(x, 1-reg)
stdlib[3] = stack_movetobottom

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

stdlib[21] = pipes_produce
