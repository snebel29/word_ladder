
words = open('/home/snebel29/word_ladder/tests/word_lists/linux_english_words_length_4').read().splitlines()

from collections import defaultdict
from itertools import product
import sys


def build_graph(words):
    buckets = defaultdict(list)
    graph = defaultdict(set)

    for word in words:
        for i in range(len(word)):
            bucket = '{}_{}'.format(word[:i], word[i + 1:])
            buckets[bucket].append(word)

    # add vertices and edges for words in the same bucket
    for bucket, mutual_neighbors in buckets.items():
        for word1, word2 in product(mutual_neighbors, repeat=2):
            if word1 != word2:
                graph[word1].add(word2)
                graph[word2].add(word1)

    return graph

graph = build_graph(words)

from collections import deque


def traverse(graph, starting_vertex):
    visited = set()
    queue = deque([[starting_vertex]])
    while queue:
        path = queue.popleft()
        vertex = path[-1]
        yield vertex, path
        for neighbor in graph[vertex] - visited:
            visited.add(neighbor)
            queue.append(path + [neighbor])

for vertex, path in traverse(graph, 'fear'):
    if vertex == 'sail':
        print(' -> '.join(path))
        sys.exit(0)

print('No path found!')
sys.exit(1)

