import uuid

import networkx as nx


def graph_from_levels(rows, level_col=2, root_id="__synthetic_root__"):
    graph = nx.DiGraph()
    graph.add_node(root_id, raw=None)

    stack = {-1: root_id}

    for row_index, row in enumerate(rows):
        level = row[level_col]
        parent_level = level - 1

        if parent_level not in stack:
            raise ValueError(f"Row {row_index}: missing parent at level {parent_level}")

        node_id = uuid.uuid4()
        attrs = {"raw": row}
        graph.add_node(node_id, **attrs)
        graph.add_edge(stack[parent_level], node_id)

        stack[level] = node_id
        stack = {key: value for key, value in stack.items() if key <= level}

    return graph


def graph_to_leafpaths(graph, root_id="__synthetic_root__", name_col=1):
    paths = []
    max_path_len = 0
    for leaf_id in [node for node in graph.nodes if node != root_id and graph.out_degree(node) == 0]:
        path = nx.shortest_path(graph, root_id, leaf_id)[1:]
        path_names = [graph.nodes[node]["raw"][name_col] for node in path]
        max_path_len = max(max_path_len, len(path_names))
        paths.append([path_names, graph.nodes[leaf_id]["raw"]])

    for index, path in enumerate(paths):
        path_names, raw = path
        paths[index] = path_names + [None] * (max_path_len - len(path_names)) + raw

    return paths
