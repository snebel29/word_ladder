import os
import unittest
from nose.tools import ok_, eq_
from word_ladder import WordLadder, Graph

word_lists_dir = os.path.dirname(__file__)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(['hello', 'hella', 'holla'])
        self.graph.build()

    def test_build(self):
        eq_(self.graph._graph['hello'], {'hella'})
        eq_(self.graph._graph['hella'], {'holla', 'hello'})
        eq_(self.graph._graph['holla'], {'hella'})

    def test_buckets(self):

        eq_(self.graph._buckets['_ello'], ['hello'])
        eq_(self.graph._buckets['h_llo'], ['hello'])
        eq_(self.graph._buckets['he_lo'], ['hello'])
        eq_(self.graph._buckets['hel_o'], ['hello'])
        eq_(self.graph._buckets['hell_'], ['hello', 'hella'])

        eq_(self.graph._buckets['_ella'], ['hella'])
        eq_(self.graph._buckets['h_lla'], ['hella', 'holla'])
        eq_(self.graph._buckets['he_la'], ['hella'])
        eq_(self.graph._buckets['hel_a'], ['hella'])

        eq_(self.graph._buckets['_olla'], ['holla'])
        eq_(self.graph._buckets['ho_la'], ['holla'])
        eq_(self.graph._buckets['hol_a'], ['holla'])
        eq_(self.graph._buckets['holl_'], ['holla'])


class TestWordLadder(unittest.TestCase):
    def setUp(self):
        self.word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'))

    def test_word_list_is_created(self):
        ok_(isinstance(self.word_ladder.words, list))

    def test_find_path_same_length(self):
        eq_(self.word_ladder.find_path('fear', 'fear'), ['fear'])
        eq_(self.word_ladder.find_path('fear', 'sail'), ['fear', 'hear', 'heir', 'hair', 'hail', 'sail'])

    def test_find_path_different_length(self):
        self.word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))
        eq_(self.word_ladder.find_path('Abe', 'Abel'), ['Abe', 'Abel'])

    def test_find_path_not_found(self):
        eq_(self.word_ladder.find_path('Abelardo', 'Abel'), None)

    def test_find_path_different_length_going_up_and_down(self):
        self.word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'fixture.1'))
        eq_(self.word_ladder.find_path('a', 'eoha'), ['a', 'ai', 'aie', 'wie', 'wieo', 'ieo', 'eo', 'eoh', 'eoha'])







