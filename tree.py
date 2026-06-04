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


def graph_to_leafpaths(graph, root_id="__synthetic_root__", path_col=1):
    paths = []
    for leaf_id in [node for node in graph.nodes if node != root_id and graph.out_degree(node) == 0]:
        path = nx.shortest_path(graph, root_id, leaf_id)[1:]
        paths.append([graph.nodes[node]["raw"][path_col] for node in path])

    return paths
