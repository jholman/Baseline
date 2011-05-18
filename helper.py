
class rstack(object):
    pass


class dstack(object):
    def __init__(self):
        self.stack = [deque()]
    def merge(self, dq, end=1):
        pass
    def split(self, n=1, end=1):
        if len(self.stack) is 0:
            # TODO: log warning
            return
        else:
            ptr = self.stack[-1*end]


class deque(object):
    # Represents a single deque, for storing arbitrary values.
    # Implementated as a doubly-linked list.

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
                self.push(i)
        elif sorted(kwargs.keys()) == ['bot','top']:
            self.end[0] = kwargs['bot']
            self.end[1] = kwargs['top']
            self.end[0].adj[0] = None
            self.end[1].adj[1] = None
        else:
            raise ValueError("deque constructor must either contain both 'top' and 'bot' keyword arguments, or none")


    def push(self, item, end=1):
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

    def pop(self, end=1):
        # Pop.  Constant-time performance.
        if self.end[end] is None:
            # TODO: log warning
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

    def _list_gen(self):
        # Helper method, returns a generator which produces the elements, from 0-end to 1-end
        todo = self.end[0]
        while todo is not None:
            yield todo
            todo = todo.adj[1]

    def __str__(self):
        return '<' + ', '.join(map(repr,self._list_gen())) + '>'

    def __repr__(self):
        return 'deque(' + ', '.join(map(lambda x: repr(x.value),self._list_gen())) + ')'



