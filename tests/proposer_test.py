import unittest

from src.Message import ProposalID, AckMessage
from src.Proposer import Proposer


class ProposerTests(unittest.TestCase):
    def setUp(self):
        self.proposer = Proposer('A', 2)

    def test_constructor(self):
        assert not self.proposer.leader
        assert self.proposer.uid == 'A'
        assert self.proposer.quorum_size == 2
        assert self.proposer.proposed_value is None
        assert self.proposer.proposal_id == ProposalID('A', 0)

    def test_propose_value(self):
        assert self.proposer.proposed_value is None
        self.proposer.propose_value(42)
        assert self.proposer.proposed_value == 42

    def test_prepare(self):
        self.proposer.proposal_id.number = 42
        message = self.proposer.prepare()
        assert message.proposal_id.number == 43
        assert len(self.proposer.ack_messages) == 0

    def test_receive_ack(self):
        self.proposer.proposal_id.number = 10
        self.proposer.propose_value(42)
        prepare_msg = self.proposer.prepare()
        ack_message = AckMessage('B', prepare_msg.proposal_id)
        self.proposer.receive_ack_message(ack_message)
        self.proposer.receive_ack_message(ack_message)
        assert len(self.proposer.ack_messages) == 1

    def test_ignore_ack_message(self):
        self.proposer.proposal_id.number = 10
        self.proposer.propose_value(42)
        self.proposer.prepare()
        ack_message = AckMessage('B', ProposalID('C', 11))
        self.proposer.receive_ack_message(ack_message)
        assert len(self.proposer.ack_messages) == 0

    def test_proposed_value_after_ack(self):
        self.proposer.proposal_id.number = 10
        self.proposer.propose_value(42)
        prepare_msg = self.proposer.prepare()
        ack_message = AckMessage('B', prepare_msg.proposal_id,
                                 ProposalID('C', 13), 44)
        self.proposer.receive_ack_message(ack_message)
        assert len(self.proposer.ack_messages) == 1
        assert self.proposer.highest_accepted_id == ProposalID('C', 13)
        assert self.proposer.proposed_value == 44
