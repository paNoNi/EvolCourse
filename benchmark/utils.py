import itertools
import json
import math
import os.path
import random
from typing import List, Tuple

from tqdm import tqdm


def generate_graph(node_count: int) -> List[Tuple[int, int]]:
    link_count = random.randint(node_count, node_count * (node_count - 1))
    graph = list()
    nodes = list(range(node_count))
    nodes_repeat = list()

    [nodes_repeat.extend(value) for value in itertools.repeat(nodes, math.ceil(link_count / node_count))]
    population_nodes_left = random.sample(nodes_repeat, k=link_count)
    population_nodes_right = random.sample(nodes_repeat, k=link_count)

    for link in range(link_count):
        node = population_nodes_left[link]
        next_node = population_nodes_right[link]
        if node != next_node:
            graph.append((node, next_node))

    return graph


def save_graph(graph: List[Tuple[int, int]], file_name: str):
    graph_json_format = dict()
    graph_json_format['nodes'] = [f'{nodes[0]}->{nodes[1]}' for nodes in graph]

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(graph_json_format, f, ensure_ascii=False, indent=4)


def generate_graphs(path_to_save: str, count_samples: int = 100, max_nodes: int = 100):
    with tqdm(total=max_nodes - 2) as t:
        for node_count in range(3, max_nodes + 1):
            for i in range(count_samples):
                new_graph = generate_graph(node_count)
                if len(new_graph) == 0:
                    continue
                save_graph(graph=new_graph, file_name=os.path.join(path_to_save, f'{i + 1}_{node_count}.json'))
            t.set_description_str('Generating...')
            t.update(1)
