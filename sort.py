import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser("args_generator")
    parser.add_argument('--path_to_graph', help='Путь к файлу с графом.', type=str, required=True)
    parser.add_argument('--type', help='[cython, python]', type=str, required=True)
    args = parser.parse_args()

    if args.type == 'python':
        from src.python_version.graph import Graph
        from src.python_version.topsort import TopologySort
    elif args.type == 'cython':
        try:
            from src.cython_version.graph import Graph
            from src.cython_version.topsort import TopologySort
        except ImportError:
            sys.exit(1)
    else:
        print('Введен неверный тип запуска. Доступны: [python. cython]')
        sys.exit(1)

    gr = Graph()
    gr.set_graph_by_config(args.path_to_graph)

    topolsort = TopologySort(gr)
    topolsort.sort()
    result_line = dict()
    for k in list(gr.nodes.keys()):
        result_line[gr.nodes[k].key] = gr.nodes[k].value

    [print(f'Priority: {pair[0]} | Value: {pair[1]}') for pair in sorted(result_line.items())]

