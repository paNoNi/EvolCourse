from typing import Any, List
import json


class Node:

    def __init__(self, value: Any, priority: int = None):
        self.priority = priority
        self.value = value
        self.next_nodes: List[Node] = list()

    def __getitem__(self, item):
        return self.next_nodes[item]

    def __len__(self):
        return len(self.next_nodes)

    def __repr__(self):
        return

    def add_next_node(self, node):
        self.next_nodes.append(node)

    def add_next_nodex(self, nodes: List):
        self.next_nodes.extend(nodes)


class Graph:

    def __init__(self):
        self.nodes = dict()

    def set_graph_by_config(self, path: str):
        with open(path) as f:
            json_conf = json.load(f)

        used_nodes = set()
        for link in json_conf['nodes']:
            nodes = link.split('->')
            for node in nodes:
                if node not in list(self.nodes.keys()):
                    self.nodes[node] = Node(node)
            self.nodes[nodes[0]].add_next_node(self.nodes[nodes[1]])

            [used_nodes.add(value) for value in nodes]

    def __getitem__(self, item):
        return self.nodes[item]

    def __len__(self):
        return len(self.nodes.keys())


