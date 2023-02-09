import cython

from src.cython_version.graph import Node, Graph

cdef get_stack(object node, dict color_map, list stack):
    color_map[node.value] = 1
    for next_node in node:
        if color_map[next_node.value] == 0:
            stack = get_stack(next_node, color_map, stack)
    color_map[node.value] = 2
    if node.value not in stack:
        stack.append(node.value)
    return stack


cdef class TopologySort:
    cdef object __graph
    cdef dict __color_map
    cdef list __stack

    def __init__(self, object graph):
        self.__graph = graph
        self.__color_map = {key: 0 for key in list(self.__graph.nodes.keys())}
        self.__stack = list()

    def sort(self):
        cdef list values = list(self.__graph.nodes.keys())
        cdef list sort_stack = list()
        for value in values:
            if value not in sort_stack:
                get_stack(self.__graph.nodes[value], self.__color_map, sort_stack)
        sort_stack = sort_stack[::-1]

        for i in range(len(sort_stack)):
            self.__graph.nodes[sort_stack[i]].priority = i + 1
