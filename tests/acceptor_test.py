import unittest

from src.Acceptor import Acceptor
from src.Message import PrepareMessage, AcceptMessage
from src.ProposalID import ProposalID
from src.Value import Value, ANY


class ProposerTests(unittest.TestCase):
    def setUp(self):
        self.acceptor = Acceptor('B')

    def test_receive_prepare(self):
        self.acceptor.promised_id = None
        self.acceptor.promised_value = None
        proposal_id = ProposalID('A', 10)
        prepare_message = PrepareMessage('A', proposal_id)
        self.acceptor.receive_prepare(prepare_message)
        assert self.acceptor.promised_id == proposal_id

    def test_receive_prepare_duplicate(self):
        proposal_id = ProposalID('A', 10)
        prepare_message = PrepareMessage('A', proposal_id)
        self.acceptor.receive_prepare(prepare_message)
        self.acceptor.receive_prepare(prepare_message)
        assert self.acceptor.promised_id == proposal_id

    def test_receive_override(self):
        proposal_id1 = ProposalID('A', 10)
        proposal_id2 = ProposalID('C', 13)
        self.acceptor.receive_prepare(PrepareMessage('A', proposal_id1))
        self.acceptor.receive_prepare(PrepareMessage('C', proposal_id2))
        assert self.acceptor.promised_id == proposal_id2

    def test_receive_ignore_when_lower(self):
        proposal_id1 = ProposalID('A', 13)
        proposal_id2 = ProposalID('C', 10)
        self.acceptor.receive_prepare(PrepareMessage('A', proposal_id1))
        self.acceptor.receive_prepare(PrepareMessage('C', proposal_id2))
        assert self.acceptor.promised_id == proposal_id1

    def test_receive_accept_initial(self):
        proposal_id = ProposalID('A', 10)
        self.acceptor.receive_prepare(PrepareMessage('A', proposal_id))
        self.acceptor.receive_accept(AcceptMessage('A', proposal_id, Value(42)))
        assert self.acceptor.promised_id == proposal_id
        assert self.acceptor.promised_value.value == 42

    def test_receive_accept_greater_than_promised(self):
        self.acceptor.receive_prepare(PrepareMessage('A', ProposalID('A', 10)))
        self.acceptor.receive_accept(
            AcceptMessage('C', ProposalID('C', 15), Value(50)))
        assert self.acceptor.promised_id == ProposalID('C', 15)
        assert self.acceptor.promised_value.value == 50

    def test_receive_request_when_having_any(self):
        self.acceptor.promised_value = ANY
        ack_value_msg = self.acceptor.receive_request(42)
        assert ack_value_msg.proposal_value.value == 42
