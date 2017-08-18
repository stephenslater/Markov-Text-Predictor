# Module that implement the xUnit paradigm
import unittest
from markov import CharIter, WordIter, char_gen, window_gen, word_gen
import markov as mar

class TestMarkov(unittest.TestCase):
    def test_table(self):
        lines = ['abc', 'def', 'ghi']
        t = mar.get_table(char_gen(lines))
        self.assertEqual(t, {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'d': 1}, 'd': {'e': 1}, 'e': {'f': 1}, 'f': {'g': 1},'g': {'h': 1}, 'h': {'i': 1}})
        
class TestWindow(unittest.TestCase):
    def test_win(self):
        lines = ['hi there', 'name is Stephen']
        # Example for size 3 words
        # hi there name
        # there name is
        # name is Stephen
        # is Stephen
        # Stephen
        res = list(window_gen(word_gen(lines), 3))
        self.assertEqual(res, [['hi', 'there', 'name'], ['there', 'name', 'is'], ['name', 'is', 'Stephen'], ['is', 'Stephen'], ['Stephen']])
        

class TestCharIter(unittest.TestCase): # parameter is parent class
    def test_basic(self):
        ci = CharIter(['a', 'b'])
        it = iter(ci)
        item = next(it)
        self.assertEqual(item, 'a')
        item = next(it)
        self.assertEqual(item, 'b')

    def test_basic2(self):
        ci = CharIter(['a', 'b', 'c'])
        res = list(ci) #O(n), has to go through and put everything in list
        self.assertEqual(res, ['a', 'b', 'c'])

    def test_gen(self):
        ci = char_gen(['a', 'b', 'c'])
        res = list(ci) #O(n), has to go through and put everything in list
        self.assertEqual(res, ['a', 'b', 'c'])

class TestWordIter(unittest.TestCase):
    def test_basic(self):
        # python will look in namespace for WordIter
        wi = WordIter(['A beautiful day', 'in the neighborhood'])
        res = list(wi)
        self.assertEqual(res, ['A', 'beautiful', 'day', 'in', 'the', 'neighborhood'])

    def test_gen(self):
        ci = word_gen(['a', 'b', 'c'])
        res = list(ci) #O(n), has to go through and put everything in list
        self.assertEqual(res, ['a', 'b', 'c'])

unittest.main()
        
