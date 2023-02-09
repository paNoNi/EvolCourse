import argparse
from benchmark.utils import generate_graphs

if __name__ == '__main__':
    parser = argparse.ArgumentParser("args_generator")
    parser.add_argument('--path_to_save', help='Путь, где сохрянятся графы.', type=str)
    parser.add_argument('--max_nodes', help='При значении N будут сгенерированы графы с 3, ..., N вершинами', type=int)
    parser.add_argument('--count_samples',
                        help='Количество примеров на каждое количество графов с определенным количеством вершин.',
                        type=int)
    args = parser.parse_args()
    generate_graphs(path_to_save=args.path_to_save, count_samples=args.count_samples, max_nodes=args.max_nodes)
