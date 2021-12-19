import numpy as np
import networkx as nx
from itertools import product
from pprint import pprint, pformat
from collections import Counter

def get_type(node):
    if node in ['start', 'end']:
        return node
    if node.isupper():
        return 'big'
    return 'small'

def is_valid(path):
    small_counts = Counter(node for node in path if get_type(node) == 'small')
    return not any(map(lambda x: x>1, small_counts.values()))

def is_valid_pt2(path):
    small_counts = Counter(node for node in path if get_type(node) == 'small')
    # print(f"{small_counts=}")
    small_over_visited = [n for n, v in small_counts.items() if v > 2]
    if len(small_over_visited) > 0:
        return False
    small_twice_visited = [n for n, v in small_counts.items() if v == 2]
    if len(small_twice_visited) > 1:
        return False
    return True

def enumerate_paths(graph, head, end):
    [start, *middle] = head
    [*middle, leading] = middle if middle else [start]
    # print(f"{head=} {middle=} {leading=} {end=}")
    paths = []

    # print(f"{nx.path_graph(graph, start, end)=}")
    # print(f"{[*nx.dfs_edges(graph, start)]=}")
    # print(f"[*graph.adjacency()]={pformat([*graph.adjacency()])}")
    # print(f"[*graph.neighbors(start)]={pformat([*graph.neighbors(start)])}")

    # for path in nx.all_simple_paths(graph, start, end):
    #     paths.append(path)

    for neighbor in graph.neighbors(leading):
        neighbor_type = get_type(neighbor)
        # print(f"{neighbor=}, {neighbor_type=}")
        if neighbor_type == 'start': continue
        if neighbor_type == 'end':
            paths.append([*head, neighbor])
            continue
        if not is_valid([*head, neighbor]):
            continue
        paths += enumerate_paths(graph, [*head, neighbor], end)
        # if following and neighbor == following:
        #     continue
    return paths

def enumerate_paths_pt2(graph, head, end):
    [start, *middle] = head
    [*middle, leading] = middle if middle else [start]
    paths = []

    for neighbor in graph.neighbors(leading):
        neighbor_type = get_type(neighbor)
        # print(f"{middle=} {leading=} {neighbor=} {end=}")
        # print(f"{neighbor=}, {neighbor_type=}")
        if neighbor_type == 'start': continue
        if neighbor_type == 'end':
            paths.append([*head, neighbor])
            continue
        if not is_valid_pt2([*head, neighbor]):
            continue
        paths += enumerate_paths_pt2(graph, [*head, neighbor], end)
        # if following and neighbor == following:
        #     continue
    return paths


def main(input):
    graph = nx.Graph()
    for [left, right] in [line.split("-") for line in input.splitlines()]:
        # print(f"{left=} {right=}")
        graph.add_node(left, t=get_type(left))
        graph.add_node(right, t=get_type(right))
        graph.add_edge(left, right)
    # paths_pt1 = enumerate_paths(graph, ["start"], "end")
    # print(f"{len(paths_pt1)=}")
    paths_pt2 = enumerate_paths_pt2(graph, ["start"], "end")
    print(f'paths ({len(paths_pt2)}):\n' + '\n'.join(map(lambda l: ','.join(map(str, l)), sorted(paths_pt2))))
    print(f"{len(paths_pt2)=}")




if __name__ == "__main__":
    EXAMPLE1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    EXAMPLE2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    EXAMPLE3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    INPUT = """pn-TY
rp-ka
az-aw
al-IV
pn-co
end-rp
aw-TY
rp-pn
al-rp
end-al
IV-co
end-TM
co-TY
TY-ka
aw-pn
aw-IV
pn-IV
IV-ka
TM-rp
aw-PD
start-IV
start-co
start-pn"""
    # main(EXAMPLE1)
    # main(EXAMPLE2)
    # main(EXAMPLE3)
    main(INPUT)
