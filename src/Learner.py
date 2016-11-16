from collections import defaultdict
from typing import Dict, Set  # noqa

from src.Message import AckValueMessage


class Learner(object):
    @property
    def completed(self):
        return self.learned_value is not None

    def __init__(self, uid: str, quorum_size: int) -> None:
        self.uid = uid
        self.quorum_size = quorum_size
        self.learned_value = None  # type: int
        self.proposals = defaultdict(
            lambda: set())  # type: Dict[int, Set[str]]

    def receive_accepted(self, ack_value_msg: AckValueMessage):
        """
        Called when receiving P2b AcceptMessage
        """
        if self.completed:
            return

        self.proposals[ack_value_msg.proposal_value].add(
            ack_value_msg.sender_uid)

        if len(self.proposals[ack_value_msg.proposal_value]) == \
                self.quorum_size:
            self.learned_value = ack_value_msg.proposal_value
