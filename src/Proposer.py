from typing import Optional, Set  # noqa

from src.Message import PrepareMessage, AckMessage, AcceptMessage
from src.ProposalID import ProposalID
from src.Value import Value, ANY


class Proposer(object):
    leader = False  # type: bool
    proposed_value = None  # type: Optional[Value]
    proposal_id = None  # type: ProposalID
    current_prepare_message = None  # type: Optional[PrepareMessage]
    current_accept_message = None  # type: Optional[AcceptMessage]

    highest_accepted_id = None  # type: Optional[ProposalID]
    ack_messages = set()  # type: Set[AckMessage]

    def __init__(self, uid: str, quorum_size: int) -> None:
        self.uid = uid
        self.quorum_size = quorum_size
        self.proposal_id = ProposalID(sender=uid, number=0)

    def propose_value(self, value: int) -> None:
        """
        Sets the proposal value for this node iff not previously set
        """
        if self.proposed_value is None:
            self.proposed_value = Value(value)

    def prepare(self) -> PrepareMessage:
        """
        Returns PrepareMessage (a.k.a P1a) with next id
        Resets received P1b messages
        """
        self.ack_messages = set()
        self.proposal_id = ProposalID(
            number=self.proposal_id.number + 1,
            sender=self.uid,
        )
        self.current_prepare_message = PrepareMessage(self.uid,
                                                      self.proposal_id)
        return self.current_prepare_message

    def receive_ack_message(self,
                            ack_message: AckMessage
                            ) -> Optional[AcceptMessage]:
        """
        Called when receiving AckMessage (a.k.a P2a)
        If a consensus is reached (majority votes) return AcceptMessage
        """
        if self._should_ignore_ack_message(ack_message):
            return None

        self.ack_messages.add(ack_message)

        if self._should_accept_proposal(ack_message):
            self.highest_accepted_id = ack_message.previous_proposal_id
            if ack_message.previous_value is not None:
                self.proposed_value = ack_message.previous_value

        if len(self.ack_messages) == self.quorum_size:
            if self._can_send_any_message():
                return AcceptMessage(self.uid, self.proposal_id, ANY)
            if self.proposed_value is not None:
                return AcceptMessage(self.uid, self.proposal_id,
                                     self.proposed_value)

    def _can_send_any_message(self):
        """
        Returns true if the proposer can send Any message to Acceptors
        """
        for ack in self.ack_messages:
            if ack.previous_value:
                return False
        return True

    def _should_ignore_ack_message(self, ack_message: AckMessage) -> bool:
        """
        Returns true if ack_message should be ignored
        i.e. the proposal_id does not match, or we have previously received
        ack from the same node
        """
        if ack_message.proposal_id != self.proposal_id:
            return True
        if ack_message in self.ack_messages:
            return True
        return False

    def _should_accept_proposal(self, ack_message: AckMessage) -> bool:
        """
        Returns true if we should select value from ack_message
        as a proposal value
        Checks if P1b message contains full proposal and the proposal number
        is the highest seen
        """
        if ack_message.previous_proposal_id is None:
            return False
        if ack_message.previous_proposal_id > self.highest_accepted_id:
            return True
        return False
