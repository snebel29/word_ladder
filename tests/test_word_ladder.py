import os
import re
import unittest
from nose.tools import ok_, eq_, raises
from word_ladder import WordLadder, Graph
from word_ladder.errors import WordsNotDefined

word_lists_dir = os.path.dirname(__file__)


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph(['hello', 'hella', 'holla'])
        cls.graph.build()

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

    def test_diff_length_build_diff_lenght_graph(self):
        graph = Graph(['Abe', 'Abel'])
        graph._build_buckets(all_lengths=True)
        eq_(sorted(graph._buckets.keys()), ['A_be', 'A_bel', 'A_e', 'A_el', 'Ab_', 'Ab_e', 'Ab_el', 'Ab_l', 'Abe_', 'Abe_l', 'Abel_', '_Abe', '_Abel', '_be', '_bel'])

    def test_same_length_build_same_lenght_graph(self):
        graph = Graph(['Abe', 'Abel'])
        graph._build_buckets(all_lengths=False)
        eq_(sorted(graph._buckets.keys()), ['A_e', 'A_el', 'Ab_', 'Ab_l', 'Abe_', 'Abel_', '_be', '_bel'])


class TestWordLadder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean_tmp_files()
        cls.word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'))

    @classmethod
    def clean_tmp_files(cls):
        for f in os.listdir(WordLadder.tmp):
            if re.search('.*_(SAME|DIFF)', f):
                os.remove(os.path.join(WordLadder.tmp, f))

    def test_find_path_caching(self):
        self.clean_tmp_files()
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'))
        word_ladder.find_path('fear', 'fear'), ['fear']
        eq_(word_ladder._retrieval_method, 'scratch')

        word_ladder.find_path('fear', 'fear'), ['fear']
        eq_(word_ladder._retrieval_method, 'memory')

        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'))
        word_ladder.find_path('fear', 'fear'), ['fear']
        eq_(word_ladder._retrieval_method, 'pickling')

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

    def test_words_has_same_length_method(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))
        eq_(word_ladder.words_has_same_length(), None)
        word_ladder.start = '1234'
        eq_(word_ladder.words_has_same_length(), None)
        word_ladder.end = '1234'
        eq_(word_ladder.words_has_same_length(), True)
        word_ladder.start = '12345'
        eq_(word_ladder.words_has_same_length(), False)

    @raises(WordsNotDefined)
    def test_start_or_end_not_defined_raises_words_not_defined_exception(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))
        word_ladder.find_path()


    def test_graph_is_reused_among_executions(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))

        word_ladder.find_path('Abe', 'Abel')
        _id = id(word_ladder.graph)
        word_ladder.find_path('Jeanne', 'sail')
        eq_(_id, id(word_ladder.graph))

        word_ladder.find_path('fear', 'sail')
        _id = id(word_ladder.graph)
        word_ladder.find_path('flux', 'fear')
        eq_(_id, id(word_ladder.graph))

    def test_graph_property(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words'))

        word_ladder.find_path('Abe', 'Abel')
        eq_(id(word_ladder._graph_diff_length), id(word_ladder.graph))

        word_ladder.find_path('flux', 'sail')
        eq_(id(word_ladder._graph_same_length), id(word_ladder.graph))

    def test_find_path_if_words_are_defined_trough_instance_variables(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'))
        word_ladder.start = 'sail'
        word_ladder.end = 'fear'
        eq_(word_ladder.find_path(), ['sail', 'hail', 'hair', 'heir', 'hear', 'fear'])

    def test_find_path_if_words_are_defined_at_instance_declaration_time(self):
        word_ladder = WordLadder(os.path.join(word_lists_dir, 'word_lists', 'linux_english_words_length_4'), 'sail', 'fear')
        eq_(word_ladder.find_path(), ['sail', 'hail', 'hair', 'heir', 'hear', 'fear'])










