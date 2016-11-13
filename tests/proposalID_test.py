from src.ProposalID import ProposalID


def test_proposal_id_equality():
    proposal_id = ProposalID('A', 10)
    assert proposal_id == proposal_id


def test_proposal_id_gt_none():
    proposal_id = ProposalID('A', 10)
    assert proposal_id > None


def test_proposal_id_ge_none():
    proposal_id = ProposalID('A', 10)
    assert proposal_id >= None


def test_proposal_id_ge():
    proposal_id1 = ProposalID('A', 10)
    proposal_id2 = ProposalID('B', 14)
    assert proposal_id2 >= proposal_id1


def test_proposal_id_gt():
    proposal_id1 = ProposalID('A', 10)
    proposal_id2 = ProposalID('B', 12)
    assert proposal_id2 > proposal_id1
