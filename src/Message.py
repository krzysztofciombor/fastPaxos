from abc import ABCMeta

from src.ProposalID import ProposalID
from src.Value import Value


class PaxosMessage(object):
    """
    Base class for all Paxos messages
    """
    __metaclass__ = ABCMeta

    # set by subclasses
    sender_uid = None  # type: str


class PrepareMessage(PaxosMessage):
    """
    P1a(n)
    """

    def __init__(self, sender_uid: str, proposal_id: ProposalID) -> None:
        self.sender_uid = sender_uid
        self.proposal_id = proposal_id


class AckMessage(PaxosMessage):
    """
    P1b(n) or P1b(n, [k, v])
    """

    def __init__(
            self,
            sender_uid: str,
            proposal_id: ProposalID,
            previous_proposal_id: ProposalID = None,
            previous_value: Value = None
    ) -> None:
        self.sender_uid = sender_uid
        self.proposal_id = proposal_id
        self.previous_proposal_id = previous_proposal_id
        self.previous_value = previous_value


class AcceptMessage(PaxosMessage):
    """
    P2a(n, v)
    """

    def __init__(self, sender_uid: str, proposal_id: ProposalID,
                 value: int) -> None:
        self.sender_uid = sender_uid
        self.proposal_id = proposal_id
        self.value = value


class AckValueMessage(PaxosMessage):
    """
    P2b(n)
    """

    def __init__(
            self,
            sender_uid: str,
            proposal_id: ProposalID,
            proposal_value: Value) -> None:
        self.sender_uid = sender_uid
        self.proposal_id = proposal_id
        self.proposal_value = proposal_value
