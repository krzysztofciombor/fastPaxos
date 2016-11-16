class ProposalID(object):
    def __init__(self, sender: str, number: int) -> None:
        self.sender = sender
        self.number = number

    def __eq__(self, other):
        return self.sender == other.sender and self.number == other.number

    def __ge__(self, other):
        if other is None:
            return True
        return self.number >= other.number

    def __gt__(self, other):
        if other is None:
            return True
        return self.number > other.number

    def __repr__(self):
        return "ProposalID(sender={}, number={})".format(self.sender,
                                                         self.number)
