import unittest

from src.Learner import Learner
from src.Message import AckValueMessage
from src.ProposalID import ProposalID


class LearnerTests(unittest.TestCase):
    def setUp(self):
        self.learner = Learner('A', 2)

    def test_basic_resolution(self):
        assert self.learner.quorum_size == 2
        self.learner.receive_accepted(
            AckValueMessage('B', ProposalID('B', 10), 42))
        assert self.learner.learned_value is None
        self.learner.receive_accepted(
            AckValueMessage('C', ProposalID('B', 10), 42))
        assert self.learner.learned_value == 42

    def test_ignore_duplicate_messages(self):
        accept_message = AckValueMessage('B', ProposalID('B', 10), 42)
        self.learner.receive_accepted(accept_message)
        self.learner.receive_accepted(accept_message)
        assert self.learner.learned_value is None

    def test_learns_value_when_quorum_is_reached(self):
        self.learner.receive_accepted(
            AckValueMessage('B', ProposalID('B', 10), 42))
        self.learner.receive_accepted(
            AckValueMessage('C', ProposalID('B', 10), 42))
        assert self.learner.learned_value == 42

    def test_learner_ignores_accept_when_already_learned(self):
        self.learner.receive_accepted(
            AckValueMessage('B', ProposalID('B', 10), 42))
        self.learner.receive_accepted(
            AckValueMessage('C', ProposalID('B', 10), 42))
        self.learner.receive_accepted(
            AckValueMessage('D', ProposalID('A', 12), 44))
        assert self.learner.learned_value == 42

    def test_learner_does_not_learn_without_quorum(self):
        self.learner.receive_accepted(
            AckValueMessage('A', ProposalID('A', 10), 42))
        self.learner.receive_accepted(
            AckValueMessage('B', ProposalID('B', 10), 10))
        assert not self.learner.completed
