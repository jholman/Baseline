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
    def test_init(self):
        ds = dstack()
        assert map(list, list(ds)) == [[]]
        ds = dstack([1, 2, 4])
        assert map(list, list(ds)) == [[1, 2, 4]]

    def test_append_and_extend(self):
        ds = dstack()
        ds.append(2)
        assert map(list, list(ds)) == [[2]]
        ds.append('q', 0)
        ds.append('r', 1)
        assert map(list, list(ds)) == [['q', 2, 'r']]
        ds.extend([3, 4], 0)
        ds.extend([5, 6], 1)
        assert map(list, list(ds)) == [[4, 3, 'q', 2, 'r', 5, 6]]

    def test_merge_split(self):
        ds = dstack([1, 2, 3])
        ds.split()
        assert map(list, ds) == [[1, 2, 3], []]
        ds.merge()
        assert map(list, ds) == [[1, 2, 3]]
        ds.merge()
        assert map(list, ds) == [[1, 2, 3]]
        ds.split(1)
        assert map(list, ds) == [[1, 2], [3]]
        ds.merge()
        ds.split(2)
        assert map(list, ds) == [[1], [2, 3]]
        ds.split(2)
        assert map(list, ds) == [[1], [], [2, 3]]
        ds.split(5)
        assert map(list, ds) == [[1], [], [], [2, 3]]
        ds.extend([4,5])
        ds.split(2,0)
        assert map(list, ds) == [[1], [], [], [4, 5], [2, 3]]
        ds.merge()
        ds.merge()
        assert map(list, ds) == [[1], [], [4, 5, 2, 3]]





