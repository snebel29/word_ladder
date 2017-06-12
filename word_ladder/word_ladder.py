import os
import hashlib
import pickle
from collections import defaultdict, deque
from itertools import product
from word_ladder.errors import WordsNotDefined

__version__ = '1.1.0'


class Graph(object):
    """
    Represents an un-weigthed graph structure with connected words

    Args:
        words (:obj:`iterable`): Words to build the graph with
    """
    def __init__(self, words):
        self._words = words
        self._graph = defaultdict(set)
        self._buckets = defaultdict(list)
        self.same_length = None

    def build(self, all_lengths=True):
        """
        Build the graph

        Args:
            all_lengths (:obj:`bool`, optional): Define if the graph should connect words with different lengths

        Returns:
            :obj:`dict` with the graph structure
        """
        self._build_buckets(all_lengths)
        self._build_graph()
        return self._graph

    def _build_buckets(self, all_lengths):
        """
        Build the necessary dictionary buckets that then will be
        used to create the dictionary word "connections"

        Notes:
            modifier is computed using all_lengths booleand parameter producing
            a range of either 1 or 2 from 1 to 0 or only 0

            modifier = 1 Append words to buckets with the same number of letter
            modifier = 0 Append words to buckets with one more letter
        """
        self.same_length = all_lengths
        self._buckets.clear()

        for word in self._words:
            for modifier in range(1, (all_lengths * -1), -1):
                for i in range(len(word)+modifier):
                    bucket = '{0}_{1}'.format(word[:i], word[i+modifier:])
                    self._buckets[bucket].append(word)

    def _build_graph(self):
        for _, neighbors in self._buckets.items():
            for word1, word2 in product(neighbors, repeat=2):
                if word1 != word2:
                    self._graph[word1].add(word2)
                    self._graph[word2].add(word1)


class WordLadder(object):
    """
    Represents a word ladder

    Args:
        dictionary (:obj:`list` or :obj:`str`): Feed with words
        start (:obj:`str`, optional): The starting word, Defaults to None
        end (:obj:`str`, optional): The ending word, Defaults to None
    """
    tmp = '/tmp'

    def __init__(self, dictionary, start=None, end=None):
        self.start = start
        self.end = end

        self._words_hash = None
        self._graph_same_length = None
        self._graph_diff_length = None

        self.words = dictionary

    @property
    def words(self):
        """
        Holds the list of words

        Returns:
            (:obj:`list`) The list of words
        """
        return self._words

    @words.setter
    def words(self, dictionary):
        if isinstance(dictionary, list):
            self._words = dictionary
        else:
            self._words = open(dictionary).read().splitlines()

        self._words_hash = hashlib.sha1(
            self._words.__str__().encode('utf-8')).hexdigest()

    def words_has_same_length(self):
        """
        Compare length of start and end words

        Note:
            when setting words an internal hash value is created for
            caching purpose, so we don't process the grah again if there is a serialzed
            version of the graph object

        Returns:
            (:obj:`bool` or :obj:`None`) True, False or None)
        """
        if self.start and self.end:
            if len(self.start) == len(self.end):
                return True
            else:
                return False
        else:
            return None

    @property
    def graph(self):
        """
        Holds an instance of :class:`Graph` with the dictionary words
        Returns:
            (:obj:`Graph`): The graph memoized instance
        """
        if self.words_has_same_length():
            kind = 'same'
            all_lengths = False
        else:
            kind = 'diff'
            all_lengths = True

        self._retrieval_method = 'memory'

        if not eval('self._graph_{0}_length'.format(kind)):
            file = os.path.join(self.tmp, self._words_hash + '_{0}'.format(kind.upper()))
            if os.path.exists(file):
                self._retrieval_method = 'pickling'
                exec('self._graph_{0}_length = pickle.load(open(file, "rb"))'.format(kind))

            else:
                self._retrieval_method = 'scratch'
                exec('self._graph_{0}_length = Graph(self.words).build(\
                                                all_lengths={1})'.format(kind, all_lengths))

                exec('pickle.dump(self._graph_{0}_length, open(file, "wb"))'.format(kind))

        return eval('self._graph_{0}_length'.format(kind))

    def find_path(self, start=None, end=None, all_paths=False):
        """
        Find the word ladder path

        Args:
            start (:obj:`str`, optional): The starting word, Defaults to None
            end (:obj:`str`, optional): The ending word, Defaults to None
            all_lengths (:obj:`bool`, optional): Define if the graph should connect words with different lengths

        Raises:
            WordsNotDefined: If any of the words is None

        Returns:
            (:obj:`list`): With the word's path or None
        """
        if start:
            self.start = start

        if end:
            self.end = end

        if not self.start or not self.end:
            raise WordsNotDefined('Either start or end is not defined')

        for vertex, path in self._walk_trough(self.start, self.graph):
            if all_paths:
                print(path)

            if vertex == self.end:
                return path

        return None

    def _walk_trough(self, start, graph):
        visited = set()
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            vertex = path[-1]
            yield vertex, path

            for neighbor in graph[vertex] - visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
