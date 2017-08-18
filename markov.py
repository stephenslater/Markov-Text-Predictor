"""
Markov chain text predictor
Coded at OpenWest Conference in Sandy, UT 7/15/17

Train model with The Adventures of Tom Sawyer:
http://www.gutenberg.org/ebooks/74
 
python3 -m idlelib.idle
 
REPL - Read, evaluate, print, loop
PEP 8 - Conventions for Python coding

Tests for call to doctest.testmod() 
>>> m = Markov('ab')
>>> m.predict('a')
'b'
 
>>> m.predict('c')
Traceback (most recent call last):
...
KeyError: 'c'
 
>>> get_table('ab')
{'a': {'b': 1}}
 
>>> random.seed(42)
>>> m2 = Markov('Find a city, find yourself a city to live in')
>>> m2.predict('c')
'i'
>>> m2.predict('i')
'n'
>>> m2.predict('t')
'o'
 
>>> test_predict(m2, 'c')
'cind a ty, citourse f'
"""
import argparse
import random
import sys
 
# An iterator needs to have a __next__
class CharIter:
    def __init__(self, lines):
        self.data = iter(lines)
        self.line = None
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        # if tries to next() pass index, python will return StopIteration exception
        while 1:
            if self.line is None:
                self.line = next(self.data)
            try:
                char = self.line[self.pos]
            except IndexError:
                self.line = next(self.data)
                self.pos = 0
            else:
                self.pos += 1
                # return goes here instead of trying to return unassigned/failed char
                # alternatively could put the self.pos += 1 and return char inside tryblock
                # but clearer to reader to see what's tried, since you know which line
                # might mess up
                return char

class WordIter(CharIter):
    def __next__(self):
        while 1:
            if self.line is None:
                self.line = next(self.data)
            try:
                # line is a string, so call split at spaces to get words
                words = self.line.split()
                word = words[self.pos]
            except IndexError:
                self.line = next(self.data)
                self.pos = 0
            else:
                self.pos += 1
                return word

# not lazy
# if accumulating into a list, make a generator
# lines is a list of strings, so lines of text
def char_gen_old(lines): 
    res = []
    for line in lines:
        for char in line:
            res.append(char)
    return res

#turn it into a list comprehension
def char_gen_lc(lines):
    res = [char for line in lines for char in line]
    return res

# same as function char_gen using LC format but still will lazily generate results
def char_gen_exp(lines):
    res = (char for line in lines for char in line) # uses () instead of []
    return res
    
#make a generator instead
def char_gen(lines): #lines is a list of strings, so lines of text
    for line in lines:
        for char in line:
            yield char

def window_gen(data, size):
    win = []
    for thing in data:
        win.append(thing)
        if len(win) == size:
            yield win
            win = win[1:]
    for i in range(len(win)):
        yield win[i:]

def word_gen(lines):
    for line in lines:
        for word in line.split():
            yield word

class Markov:
    """
    >>> m3 = Markov('Find a city, find yourself a city to live in', 3)
    >>> m3.predict('cit')
    'y'
    """
    def __init__(self, data, size=1):
        #self.table = get_table(data)
        self.tables = []
        for i in range(size):
            self.tables.append(get_table(data, i+1))
         
    def predict(self, data_in):
        table = self.tables[len(data_in)-1]
        options = table[data_in]
        possible = ''
        for key, count in options.items():
            possible += key * count
        return random.choice(possible)

class CharMarkov(Markov):
    """
    >>> lines = ['abc', 'def', 'hi']
    >>> cm = CharMarkov(lines, 2)
    >>> cm.predict('cd')
    'e'
    """
    def __init__(self, lines, size=1):
        self.tables = []
        data = list(char_gen(lines))
        for i in range(size):
            self.tables.append(get_table(data, i + 1))

class WordMarkov(Markov):
    """
    >>> lines = ['my name is', 'Stephen', 'Hello!']
    >>> wm = WordMarkov(lines, 2)
    >>> wm.predict('is')
    'Stephen'
    """
    def __init__(self, lines, size=1):
        self.tables = []
        data = list(word_gen(lines))
        for i in range(size):
            self.tables.append(get_table(data, i + 1))

    def predict(self, data_in):
        table = self.tables[len(data_in.split())-1]
        options = table[data_in]
        possible = []
        for key, count in options.items():
            for i in range(count):
                possible.append(key)
        return random.choice(possible)

def test_predict(m, start, numchars=1):
    res = [start]
    for i in range(20):
        let = m.predict(start)
        res.append(let)
        start = ''.join(let[-numchars:])
    return ''.join(res)
         
def get_table_old(line, numchars=1):
    result = {}
    for i, _ in enumerate(line):
        chars = line[i:i+numchars]
        try:
            next_char = line[i+numchars]
        except IndexError:
            break
        char_dict = result.get(chars, {})
        char_dict.setdefault(next_char, 0)
        char_dict[next_char] += 1
        result[chars] = char_dict
    return result

def get_table(data, size = 1, join_char=''):
    results = {}
    for tokens in window_gen(data, size + 1):
        item = join_char.join(tokens[:size])
        try:
            output = tokens[size]
        except IndexError:
            break
        inner_dict = results.get(item, {})
        inner_dict.setdefault(output, 0)
        inner_dict[output] += 1
        results[item] = inner_dict
    return results

# REPL to predict text based on input and trained text
def repl(m):
    while 1:
        try:
            txt = input(">")
        except KeyboardInterrupt:
            break
        try:
            res = m.predict(txt)
        except KeyError:
            print("This text does not appear in my dictionary: " + txt)
            continue
        print(res)
 
def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='input file')
    p.add_argument('-s', '--size', help="Markov size",
                   default=1, type=int)
    p.add_argument('--encoding', help='File encoding',
                   default='utf8')
    p.add_argument('-t', '--test', action='store_true', help='Run tests')
    opt = p.parse_args(args)
    if opt.file:
        with open(opt.file, encoding=opt.encoding) as fin:         
            data = fin.read()
            m = Markov(data, size=opt.size)
            repl(m)
    elif opt.test:
        import doctest
        doctest.testmod()

# Run Markov REPL from the command line
if __name__ == '__main__':
    # Whether to execute tests
    # import doctest
    # doctest.testmod()
    main(sys.argv[1:])
else:
    print("not running")
