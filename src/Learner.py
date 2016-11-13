from collections import defaultdict
from typing import Dict, Set  # noqa

from src.Message import AcceptMessage


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

    def receive_accepted(self, accept_message: AcceptMessage):
        """
        Called when receiving P2b AcceptMessage
        """
        if self.completed:
            return

        self.proposals[accept_message.value].add(accept_message.sender_uid)

        if len(self.proposals[accept_message.value]) == self.quorum_size:
            self.learned_value = accept_message.value
