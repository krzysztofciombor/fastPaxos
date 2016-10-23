def get_classic_quorum_size(nodes_count: int) -> int:
    return nodes_count // 2 + 1


def get_fast_quorum_size(nodes_count: int) -> int:
    return 3 * nodes_count // 4
