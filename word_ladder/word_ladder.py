from collections import defaultdict, deque
from itertools import product
from word_ladder.errors import WordsNotDefined

__version__ = '0.0.1'


class Graph(object):
    def __init__(self, words):
        self._words = words
        self._graph = defaultdict(set)
        self._buckets = defaultdict(list)

    def build(self, all_lengths=True):
        self._build_buckets(all_lengths)
        self._build_graph()
        return self._graph

    def _build_buckets(self, all_lengths):
        """
        modifier = 1 - Append words to buckets with the same number of letter
        modifier = 0 - Append words to buckets with one more letter
        """
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
    def __init__(self, dictionary, start=None, end=None):
        if isinstance(dictionary, list):
            self.words = dictionary
        else:
            self.words = open(dictionary).read().splitlines()

        self.start = start
        self.end = end

        self._graph_same_length = None
        self._graph_diff_length = None

    def words_has_same_length(self):
        if self.start and self.end:
            if len(self.start) == len(self.end):
                return True
            else:
                return False
        else:
            return None

    @property
    def graph(self):
        if self.words_has_same_length():
            if not self._graph_same_length:
                self._graph_same_length = Graph(self.words).build(
                                                    all_lengths=False)

            return self._graph_same_length

        else:
            if not self._graph_diff_length:
                self._graph_diff_length = Graph(self.words).build(
                                                    all_lengths=True)

            return self._graph_diff_length

    def find_path(self, start=None, end=None, all_paths=False):
        if start:
            self.start = start

        if end:
            self.end = end

        if not start or not end:
            raise WordsNotDefined('Either start or end is not defined')

        for vertex, path in self._walk_trough(start, self.graph):
            if all_paths:
                print(path)

            if vertex == end:
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
