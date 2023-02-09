import argparse
import collections
import os
import time

from matplotlib import pyplot as plt
from tqdm import tqdm

from benchmark.utils import generate_graphs

STAGES = 10


def bench_wrapper(args, is_cython: bool = 1):
    if is_cython:
        try:
            from src.cython_version.graph import Graph
            from src.cython_version.topsort import TopologySort
        except ImportError:
            print('Ooops...')
    else:
        from src.python_version.graph import Graph
        from src.python_version.topsort import TopologySort

    full_nodecount_time = dict()

    for s in range(STAGES):
        whole_time = 0
        nodecount_time = dict()
        nodecount_count = dict()
        generate_graphs(path_to_save=args.path_to_save, count_samples=args.count_samples, max_nodes=args.max_nodes)
        graphs_files = os.listdir(args.path_to_save)
        with tqdm(total=len(graphs_files)) as t:
            for i, graph_file in enumerate(graphs_files):
                graph = Graph()
                graph.set_graph_by_config(os.path.join(args.path_to_save, graph_file))
                top_sort = TopologySort(graph)
                per_sort_time = time.time()
                top_sort.sort()
                per_sort_time = (time.time() - per_sort_time) * 1_000
                whole_time += per_sort_time
                node_count = graph_file[graph_file.index('_') + 1: graph_file.index('.json')]
                node_count = int(node_count)

                nodecount_time_keys = nodecount_time.keys()
                if node_count not in list(nodecount_time_keys):
                    nodecount_count[node_count] = 0
                    nodecount_time[node_count] = 0

                nodecount_count[node_count] = nodecount_count[node_count] + 1
                full_time_node_count = nodecount_time[node_count] * nodecount_count[node_count] + per_sort_time
                nodecount_time[node_count] = full_time_node_count / (nodecount_count[node_count] + 1)
                t.set_postfix_str(f'Mean time on graph: {whole_time / (i + 1)} Sec. * 10^(-3)')
                t.set_description_str(f'Stage: {s + 1}')
                t.update(1)

        for key in list(nodecount_count.keys()):
            if key not in list(full_nodecount_time.keys()):
                full_nodecount_time[key] = 0
            full_nodecount_time[key] += nodecount_time[key]

    for key in list(full_nodecount_time.keys()):
        full_nodecount_time[key] = full_nodecount_time[key] / STAGES

    return collections.OrderedDict(sorted(full_nodecount_time.items()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("args_generator")
    parser.add_argument('--type', help='[cython, python]', type=str, required=True)
    parser.add_argument('--path_to_save', help='Путь, где сохрянятся графы.', type=str)
    parser.add_argument('--max_nodes', help='При значении N будут сгенерированы графы с 3, ..., N вершинами', type=int)
    parser.add_argument('--count_samples',
                        help='Количество примеров на каждое количество графов с определенным количеством вершин.',
                        type=int)
    args = parser.parse_args()

    ods = bench_wrapper(args), bench_wrapper(args, is_cython=False)
    fig, ax = plt.subplots(nrows=1, ncols=1)

    nodes_count = list(ods[0].keys())
    ax.plot(nodes_count, list(ods[0].values()), label='cython version')
    ax.plot(nodes_count, list(ods[1].values()), label='python version')
    ax.set_xlabel('Количество вершин')
    ax.set_ylabel('Среднее время работы. Сек. * 10^(-3)')
    ax.set_title('Время работы двух версий')
    ax.legend()
    fig.savefig('adv_data\\graphic.png')
