import json

cdef class Node:
    cdef public int priority
    cdef public int value
    cdef public list next_nodes
    cdef public Node node
    cdef dict __dict__

    def __cinit__(self, value not None):
        self.priority = -1
        self.value = value
        self.next_nodes = list()

    def __getitem__(self, item):
        return self.next_nodes[item]

    def __len__(self):
        return len(self.next_nodes)

    cdef add_next_node(self, node):
        self.next_nodes.append(node)

    cdef add_next_nodex(self, nodes):
        self.next_nodes.extend(nodes)

cdef class Graph:
    cdef public dict nodes
    cdef public dict json_conf
    cdef public list pair_nodes
    cdef dict __dict__

    def __cinit__(self):
        self.nodes = dict()

    cdef set_graph_by_config(self, str path):

        with open(path) as f:
            json_conf = dict(json.load(f))

        cdef set used_nodes = set()
        for link in json_conf['nodes']:
            pair_nodes = link.split('->')
            pair_nodes = [int(val) for val in pair_nodes]
            for node in pair_nodes:
                if node not in list(self.nodes.keys()):
                    self.nodes[node] = Node(node)
            self.nodes[pair_nodes[0]].add_next_node(self.nodes[pair_nodes[1]])

            [used_nodes.add(value) for value in pair_nodes]

    def __getitem__(self, int item):
        return self.nodes[item]

    def __len__(self):
        return len(self.nodes.keys())
