from src.Acceptor import Acceptor
from src.Proposer import Proposer
from src.Learner import Learner
from src.Message import PrepareMessage, AcceptMessage, AckMessage, AckValueMessage

from typing import Optional
from src.HttpClient import HttpClient
from src.ProposalID import ProposalID
from IPython import embed  # type: ignore

class Instance(object):
    active = True  # type: bool
    http_client = HttpClient()  # type: HttpClient

    def __init__(self, uid: str, quorum_size: int) -> None:
        self.uid = uid
        self.quorum_size = quorum_size
        self.proposer = Proposer(self.uid, self.quorum_size)
        self.acceptor = Acceptor(self.uid)
        self.learner = Learner(self.uid, self.quorum_size)


    def get_active(self):
        return self.active

    # Proposer methods delegation

    def propose_value(self, value: int) -> None:
        self.proposer.propose_value(value)

    def prepare(self) -> PrepareMessage:
        return self.proposer.prepare()

    def receive_ack_message(self,
                            ack_message: AckMessage
                            ) -> Optional[AcceptMessage]:

        return self.proposer.receive_ack_message(ack_message)

    # Acceptor methods delegation

    def receive_prepare(self, prepare_message: PrepareMessage) -> AckMessage:
        return self.acceptor.receive_prepare(prepare_message)

    def receive_accept(self, accept_message: AcceptMessage) \
                -> Optional[AckValueMessage]:
        return self.acceptor.receive_accept(accept_message)


    # Learner methods delegation

    def receive_accepted(self, accept_message: AcceptMessage):
        self.learner.receive_accepted(accept_message)
