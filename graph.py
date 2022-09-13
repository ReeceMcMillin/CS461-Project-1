from collections import defaultdict
from dataclasses import dataclass
from math import sqrt
from typing import List, Set, Tuple
import heapq


def manhattan_distance(src: Tuple, dest: Tuple):
    return sqrt(abs(src[0] - dest[0]) + abs(src[1] - dest[1]))


def backtrack(came_from: dict, city: str):
    path = [city]
    while came_from.get(city) is not None:
        city = came_from.get(city)
        path.append(city)
    return list(reversed(path))


@dataclass
class Node:
    name: str
    location: Tuple[float, float]

    def __eq__(self, other: "Node") -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Edge:
    src: Node
    dest: Node
    weight: float

    def inverse(self) -> "Edge":
        return Edge(self.dest, self.src, self.weight)


class Graph:
    def __init__(self, nodes: List[Node], edges: List[Edge], directed=False):
        self.nodes = nodes
        if directed:
            self.edges = edges
        else:
            self.edges = [
                edge for pair in [(e, e.inverse()) for e in edges] for edge in pair
            ]

    def neighbors(self, src: str) -> Set[Node]:
        return {edge.dest for edge in self.edges if edge.src.name == src}

    def get_node(self, name: str) -> Node:
        node_names = list(map(lambda x: x.name, self.nodes))
        if name in node_names:
            return self.nodes[node_names.index(name)]

    def a_star(self, start: str, goal: str):
        """Mostly translated from Wikipedia's pseudocode for A*
        https://en.wikipedia.org/wiki/A*_search_algorithm"""

        start_node: Node = self.get_node(start)
        goal_node: Node = self.get_node(goal)

        came_from = dict()

        g_score = defaultdict(lambda: float("inf"))
        f_score = defaultdict(lambda: float("inf"))

        heuristic = lambda node: manhattan_distance(node.location, goal_node.location)

        g_score[start] = 0
        f_score[start] = heuristic(start_node)

        open_set = [(f_score[start], start)]

        while current := heapq.heappop(open_set):
            current_node = self.get_node(current[1])

            if current_node.name == goal:
                print(" -> ".join(backtrack(came_from, current_node.name)))
                return

            for neighbor in self.neighbors(current_node.name):
                tentative_g_score = g_score[current_node.name] + manhattan_distance(
                    current_node.location, neighbor.location
                )

                if tentative_g_score < g_score[neighbor.name]:
                    came_from[neighbor.name] = current_node.name
                    g_score[neighbor.name] = tentative_g_score
                    f_score[neighbor.name] = tentative_g_score + heuristic(neighbor)

                    if neighbor.name not in map(lambda x: x[1], open_set):
                        heapq.heappush(
                            open_set, (f_score[neighbor.name], neighbor.name)
                        )
        print("No paths found.")
        return False
