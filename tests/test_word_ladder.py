import os
import unittest
from nose.tools import ok_, eq_
from word_ladder import WordLadder

word_lists_dir = os.path.dirname(__file__)

class TestWordLadder(unittest.TestCase):
    def setUp(self):
        self.word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))

    def test_word_list_is_created(self):
        ok_(isinstance(self.word_ladder.words, list))

    def test_find(self):
        eq_(self.word_ladder.find('hello', 'halla'), ['hello', '', 'halla'])

