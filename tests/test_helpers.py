import unittest

from baseline.helper import deque, dstack, rstack


class TestDeque():
    def test_append_and_iter(self):
        d = deque()
        d.append(1)
        d.append('b')
        d.append([[],[],[]])
        assert list(d) == [1, 'b', [[],[],[]]]
        d.append('', 0)
        d.append(4)
        d.append('negative one', 0)
        assert list(d) == ['negative one', '', 1, 'b', [[],[],[]], 4]

    def test_init_and_pop(self):
        d = deque(1,2,3,4)
        d.append(5)
        d.append(0,0)
        d.append(6)
        d.append(-1,0)
        x = d.pop()
        x = d.pop()
        x = d.pop()
        assert x == 4
        x = d.pop(0)
        x = d.pop(0)
        x = d.pop()
        x = d.pop(0)
        assert x == 1

    def test_len_and_extend(self):
        d = deque()
        assert len(d) == 0
        d.append(1,0)
        assert len(d) == 1
        d.extend(['a','b','c'])
        assert len(d) == 4
        x = d.pop(0)
        x = d.pop(0)
        assert x == 'a'
        assert len(d) == 2


class TestDStack():
    pass


