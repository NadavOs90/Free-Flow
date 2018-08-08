import networkx as nx
import random
import itertools
from termcolor import colored


class Board(object):
    def __init__(self, size=5, pairs=None):
        self._size = size
        self._vortexes = self._get_vortexes()
        self._graph = self._build_graph()
        self._pairs = self._select_pairs(pairs)
        self._paths = self._get_all_simple_paths()
        self._c = '{} '.format(unichr(57934).encode('utf-8'))
        self._p = '{} '.format(unichr(57935).encode('utf-8'))
        self._color_map = {}

    def _build_graph(self):
        G = nx.Graph()
        G.add_nodes_from(self._vortexes)
        G.add_edges_from(self._get_edges())
        return G

    def _select_pairs(self, pairs):
        if pairs is None:
            pairs = []
            vortexes = self._get_vortexes()
            while len(pairs) < self._size:
                s = random.choice(vortexes)
                vortexes.remove(s)
                t = random.choice(vortexes)
                vortexes.remove(t)
                pairs.append((s, t))
        elif isinstance(pairs[0][0], tuple):
            pairs = map(lambda pair: self._convert_to_vortex_pair(pair), pairs)
        return pairs

    def _get_vortexes(self):
        return range(1, (self._size ** 2) + 1)

    def _vortex_is_on_boarder(self, v):
        neighbors = 0
        up = v - self._size
        down = v + self._size
        left = v - 1
        right = v + 1
        if down in self._vortexes:
            neighbors += 1
        if up in self._vortexes:
            neighbors += 1
        if left in self._vortexes and left % self._size != 0:
            neighbors += 1
        if right in self._vortexes and right % self._size != 1:
            neighbors += 1
        return neighbors < 4

    def _path_is_on_boarder(self, path):
        return all(self._vortex_is_on_boarder(v) for v in path)

    def _get_edges(self):
        edges = []
        for v in self._vortexes:
            down = v + self._size
            right = v + 1
            if down in self._vortexes:
                edges.append((down, v))
            if right in self._vortexes and right % self._size != 1:
                edges.append((right, v))
        return list(set(edges))

    def _get_all_simple_paths(self):
        paths = {}
        for pair in self._pairs:
            cutoff = self._get_cutoff(pair)
            selected = [i for sub in self._pairs for i in sub if i not in pair]
            paths[pair] = []
            three_path_flag = False
            simple_paths_gen = nx.all_simple_paths(self._graph, source=pair[0], target=pair[1], cutoff=cutoff)
            for path in simple_paths_gen:
                if len(path) == 3:
                    if not three_path_flag:
                        three_path_flag = True
                        paths[pair] = [path]
                    else:
                        paths[pair].append(path)
                elif not three_path_flag and set(path).isdisjoint(selected):
                    paths[pair].append(path)
        return paths

    @staticmethod
    def _has_duplicates(flat_list_of_values):
        temp = list(set(flat_list_of_values))
        return len(temp) != len(flat_list_of_values)

    def _check_solution(self, solution):
        flat_list = [i for j in solution for i in j]
        if len(flat_list) != self._size**2 or self._has_duplicates(flat_list):
            return False
        return True

    def _get_solution(self):
        for pair, paths in self._paths.iteritems():
            if self._vortex_is_on_boarder(pair[0]) and self._vortex_is_on_boarder(pair[1]):
                boarder_paths = filter(lambda path: self._path_is_on_boarder(path), paths)
                self._paths[pair] = boarder_paths if len(boarder_paths) > 0 else paths
        all_paths = self._paths.values()
        all_combinations = list(itertools.product(*all_paths))
        all_combinations = filter(lambda comb: self._check_solution(comb), all_combinations)
        all_combinations = map(lambda solution: list(solution), all_combinations)
        return 'No Solution' if all_combinations == [] else all_combinations

    def solve(self):
        solutions = self._get_solution()
        print 'Pairs: ', self._pairs
        if isinstance(solutions, list):
            print 'Solution: '
            for solution in solutions:
                print solution
            return True
        print solutions
        return False

    def print_board(self):
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan', 'grey', 'white']
        graph_nodes = self._graph.nodes()
        nodes = []
        for node in graph_nodes:
            nodes.append(node)
        pairs = self._pairs
        for pair in pairs:
            color = random.choice(colors)
            colors.remove(color)
            self._color_map[pair] = color
            nodes = map(lambda x: colored(self._p, color) if x in pair else x, nodes)
        graph = [nodes[x:x + self._size] for x in xrange(0, len(nodes), self._size)]
        for row in graph:
            row = map(lambda x: self._c if isinstance(x, int) else x, row)
            print ' '.join(row)

    def print_board_with_solution(self):
        solutions = self._get_solution()
        if isinstance(solutions, list):
            solution = solutions[0]
        else:
            print solutions
            return
        graph_nodes = self._graph.nodes()
        nodes = []
        for node in graph_nodes:
            nodes.append(node)
        pairs = self._pairs
        for pair in pairs:
            color = self._color_map[pair]
            for path in solution:
                if pair[0] in path and pair[1] in path:
                    break
            nodes = map(lambda x: colored(self._p, color) if x in pair else x, nodes)
            nodes = map(lambda x: colored(self._c, color) if x in path else x, nodes)
        graph = [nodes[x:x + self._size] for x in xrange(0, len(nodes), self._size)]
        for row in graph:
            row = map(lambda x: self._c if isinstance(x, int) else x, row)
            print ' '.join(row)

    def _get_cutoff(self, pair):
        cutoff = self._size ** 2 - 1
        for pair2 in self._pairs:
            if pair != pair2:
                cutoff -= nx.shortest_path_length(self._graph, pair2[0], pair2[1]) + 1
        return cutoff

    def _convert_to_vortex_pair(self, pair):
        return self._convert_to_vortex(pair[0]), self._convert_to_vortex(pair[1])

    def _convert_to_vortex(self, coordinates):
        return coordinates[0] * self._size + coordinates[1] + 1


