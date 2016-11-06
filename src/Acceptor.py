from typing import Optional

from src.Message import PrepareMessage, AckMessage, AcceptMessage, \
    AckValueMessage
from src.ProposalID import ProposalID  # noqa
from src.Value import Value


class Acceptor(object):
    promised_id = None  # type: Optional[ProposalID]
    promised_value = None  # type: Optional[Value]

    def __init__(self, uid: str) -> None:
        self.uid = uid

    def receive_prepare(self, prepare_message: PrepareMessage) -> AckMessage:
        """
        Called when receiving P1a PrepareMessage
        Returns P1b AckMessage which may contain current promise
        """
        if prepare_message.proposal_id > self.promised_id:
            self.promised_id = prepare_message.proposal_id
            return AckMessage(self.uid, self.promised_id)
        else:
            return AckMessage(self.uid,
                              prepare_message.proposal_id,
                              self.promised_id,
                              self.promised_value)

    def receive_accept(self,
                       accept_message: AcceptMessage
                       ) -> Optional[AckValueMessage]:
        """
        Called when receiving P21 AcceptMessage
        Returns P2b AckValueMessage
        """
        if accept_message.proposal_id >= self.promised_id:
            self.promised_id = accept_message.proposal_id
            self.promised_value = accept_message.value
            return AckValueMessage(self.uid,
                                   self.promised_id,
                                   self.promised_value)

    def receive_request(self, value: int) -> Optional[AckValueMessage]:
        """
        FAST PAXOS
        Called when receiving value request directly from client
        If we've got an any message from proposer previously,
        we are free to propose this value
        """
        if self.promised_value and self.promised_value.is_any:
            return AckValueMessage(self.uid,
                                   ProposalID(self.uid, 0),
                                   Value(value))
