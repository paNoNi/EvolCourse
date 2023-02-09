from typing import List

from src.python_version.graph import Graph, Node
try:
    from src.cython_version.topology import get_stack as cget_stack
except ImportError:
    print('Ooops...')

def get_stack(node: Node, color_map: dict, stack: List) -> List:
    color_map[node.value] = 1
    for next_node in node:
        if color_map[next_node.value] == 0:
            stack = get_stack(next_node, color_map, stack)
    color_map[node.value] = 2
    if node.value not in stack:
        stack.append(node.value)
    return stack


class TopologySort:

    def __init__(self, graph: Graph):
        self.__graph = graph
        self.__color_map = {key: 0 for key in list(self.__graph.nodes.keys())}
        self.__stack = list()

    def sort(self):
        values = list(self.__graph.nodes.keys())

        sort_stack = list()
        for value in values:
            if value not in sort_stack:
                get_stack(self.__graph.nodes[value], self.__color_map, sort_stack)
        sort_stack = sort_stack[::-1]

        for i in range(len(sort_stack)):
            self.__graph.nodes[sort_stack[i]].key = i + 1

