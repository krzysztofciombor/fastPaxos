from src.Paxos import get_classic_quorum_size, get_fast_quorum_size


def test_classic_quorum_size():
    assert get_classic_quorum_size(4) == 3
    assert get_classic_quorum_size(5) == 3
    assert get_classic_quorum_size(8) == 5


def test_fast_quorum_size():
    assert get_fast_quorum_size(3) == 2
    assert get_fast_quorum_size(4) == 3
    assert get_fast_quorum_size(5) == 3
    assert get_fast_quorum_size(8) == 6
