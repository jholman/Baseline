
class rstack(list):
    pass

class dstack(object):
    def __init__(self, iterable = ()):
        self.stack = [deque(*iterable)]

    def __str__(self):
        return '\n'.join(map(str,reversed(self.stack)))

    def merge(self, end=1, reverse=False):
        if reverse:
            raise NotImplementedError # should log ERROR, because it's not implemented!  # TODO: implement
        if len(self.stack) < 2:
            return # should log INFO probably
        if self.stack[-1].end == [None, None]:
            self.stack.pop()
        elif self.stack[-2].end == [None, None]:
            self.stack.pop(-2)
        else:
            old_car_bottom = self.stack[-1].end[1-end]
            old_cadr_top = self.stack[-2].end[end]
            old_car_bottom.adj[1-end] = old_cadr_top
            old_cadr_top.adj[end] = old_car_bottom
            self.stack[-2].end[1] = self.stack[-1].end[1]
            self.stack.pop()

    def split(self, n=0, end=1):    # ('end' marks which end of the top deque)
        if len(self.stack) is 0:
            return # should log ERROR, stack should never be empty
        elif n == 0:            # just want a new empty deque
            self.stack.append(deque())
            return
        elif self.stack[-1].end == [None, None]:
            self.stack.append(deque())
            return
        else:
            topdeque = self.stack[-1]
            ptr = topdeque.end[end]
            for i in range(n-1):
                if not ptr.adj[1-end]:
                    break
                ptr = ptr.adj[1-end]
            if ptr.adj[1-end]:
                ptr = ptr.adj[1-end]            # now ptr is out of the split-section
                ptr.adj[end].adj[1-end] = None
                self.stack.append(deque(top=topdeque.end[end], bot=ptr.adj[end]))
                ptr.adj[end] = None
                self.stack[-2].end[end] = ptr
            else:
                self.stack.insert(-1, deque())
                pass

    def append(self, item, end=1):
        if len(self.stack) is 0:
            return          # should log ERROR, stack should never be empty
        try:
            for i in item:
                self.append(i, end)
        except:
            self.stack[-1].append(item, end)

    def pop(self, end=1, n=1):
        if len(self.stack) is 0:
            # should log ERROR, stack should never be empty
            return
        ans = []
        for i in range(n):
            ans.append(self.stack[-1].pop(end))
        return ans


class deque(object):
    """A polymorphic double-ended queue, implemented as a linked list.

    Attempts to copy the interface of the built-in list object as much as
    possible, including iterability and most container behaviour."""

    class elt(object):
        # Utility class to encapsulate the inter-element links
        def __init__(self, value, prev=None, succ=None):
            self.value = value
            self.adj = [prev, succ]
        def __repr__(self):
            return repr(self.value)
        def __str__(self):
            return str(self.value)

    def __init__(self, *argv, **kwargs):
        # Constructor.  Optionally takes EITHER:
        #       two keyword argments, 'top' and 'bottom', pointing to elts, or
        #       0 or more arguments containining initialization elements
        self.end = [None,None]
        if kwargs.keys() == []:
            for i in argv:
                self.append(i)
        elif sorted(kwargs.keys()) == ['bot','top']:
            self.end[0] = kwargs['bot']
            self.end[1] = kwargs['top']
            self.end[0].adj[0] = None
            self.end[1].adj[1] = None
        else:
            raise ValueError("deque constructor must either contain both 'top' and 'bot' keyword arguments, or none")

    def append(self, item, end=1):
        # Push.  Constant-time performance.
        if end not in [0,1]:
            raise IndexError("%s is not a valid end-index for a deque (valid: 0 or 1)" % end)
        if self.end == [None, None]:
            self.end[0] = self.end[1] = self.elt(item)
        else:
            tmpend = self.end[end]
            self.end[end] = self.elt(item)
            tmpend.adj[end] = self.end[end]
            self.end[end].adj[1-end] = tmpend

    def extend(self, iterable, end=1):
        for i in iterable:
            self.append(i, end)

    def pop(self, end=1):
        # Pop.  Constant-time performance.
        if self.end[end] is None:
            # should log DEBUG: it's legal but might not be intended
            return None
        else:
            ans = self.end[end].value
        if self.end[end].adj[1-end] is None:
            self.end = [None,None]
        else:
            self.end[end] = self.end[end].adj[1-end]
            self.end[end].adj[end].adj[1-end] = None
            self.end[end].adj[end] = None
        return ans

    def __iter__(self, direction=1):       # direction=1 for left-to-right
        todo = self.end[1-direction]
        while todo is not None:
            yield todo.value
            todo = todo.adj[direction]

    def __reversed__(self):
        return self.__iter__(0)

    def __str__(self):
        return '<' + ', '.join(map(repr,self.__iter__())) + '>'

    def __repr__(self):
        return 'deque(' + ', '.join(map(lambda x: repr(x.value),self.__iter__())) + ')'

    def __len__(self):
        ans = 0
        todo = self.end[0];
        while todo is not None:
            ans += 1
            todo = todo.adj[1]
        return ans




