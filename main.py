from collections import ChainMap
from functools import partial, reduce
from graph import Graph, Edge, Node, manhattan_distance


with open("coordinates.txt") as f:
    coordinates = reduce(
        lambda x, y: y(x),
        [
            partial(map, str.strip),
            partial(map, str.split),
            partial(map, lambda x: {x[0]: tuple(map(float, x[1:]))}),
            partial(lambda mapping: ChainMap(*mapping)),
            dict,
        ],
        f.readlines(),
    )

with open("Adjacencies.txt") as f:
    adjacencies = reduce(
        lambda x, y: y(x),
        [
            partial(map, partial(str.strip)),
            partial(map, partial(str.split)),
            partial(map, list),
            list,
        ],
        f.readlines(),
    )

edges = []

for city in adjacencies:
    for neighbor in city[1:]:
        src = Node(city[0], coordinates[city[0]])
        dest = Node(neighbor, coordinates[neighbor])
        edges.append(Edge(src, dest, manhattan_distance(src.location, dest.location)))

nodes = [Node(city, coordinates[city]) for city in coordinates.keys()]

g = Graph(nodes, edges)


if __name__ == "__main__":
    while (start := input("Start: ")) not in coordinates.keys():
        print("Error: unrecognized city.")

    while (goal := input("Goal: ")) not in coordinates.keys():
        print("Error: unrecognized city.")

    g.a_star(start, goal)
