from collections import defaultdict, deque
from itertools import product


class Graph(object):
    def __init__(self, words):
        self._words = words
        self._graph = defaultdict(set)
        self._buckets = defaultdict(list)

    def build(self):
        self._build_buckets()
        self._build_graph()
        return self._graph

    def _build_buckets(self):
        for word in self._words:
            for i in range(len(word)):
                bucket = '{}_{}'.format(word[:i], word[i+1:])
                self._buckets[bucket].append(word)

    def _build_graph(self):
        for bucket, neighbors in self._buckets.items():
            for word1, word2 in product(neighbors, repeat=2):
                if word1 != word2:
                    self._graph[word1].add(word2)
                    self._graph[word2].add(word1)


class WordLadder(object):
    def __init__(self, path):
        self.words = open(path).read().splitlines()
        self.graph = Graph(self.words).build()

    def find_path(self, start, end):
        for vertex, path in self._walk_trough(start):
            if vertex == end:
                return path

        return None

    def _walk_trough(self, start):
        visited = set()
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            vertex = path[-1]
            yield vertex, path
            for neighbor in self.graph[vertex] - visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
