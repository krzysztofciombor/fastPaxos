from IPython import embed  # type: ignore
import requests  # type: ignore
from src.Message import PrepareMessage, AckMessage, AcceptMessage, AckValueMessage
from src.ProposalID import ProposalID
from typing import Optional

class HttpClient(object):
    # change on production
    host = "http://127.0.0.1:5000"
    base_url = host + "/internal_api/instances/"

    def get_heartbeat(self, instance_id: str):
        return requests.get(self._instance_url(instance_id) + '/heartbeat').json()

    def get_prepare(self, instance_id: str) -> PrepareMessage:
        result = requests.get(self._instance_url(instance_id) + '/prepare').json()

        prepare_message_json = result['PrepareMessage']
        proposal_id_json = prepare_message_json['proposal_id']

        proposal_id = ProposalID(proposal_id_json['sender'], proposal_id_json['number'])
        return PrepareMessage(prepare_message_json['sender_uid'], proposal_id)

    def post_value(self, instance_id: str, value: int) -> None:
        requests.post(self._instance_url(instance_id) + '/value',
                      data = { 'value': value })

    def post_ack_message(self, instance_id: str, ack_message: AckMessage) -> Optional[AcceptMessage]:
        previous_proposal_id = ack_message.previous_proposal_id
        previous_proposal_id_sender = None
        previous_proposal_id_number = None

        if previous_proposal_id is not None:
            previous_proposal_id_sender = previous_proposal_id.sender
            previous_proposal_id_number = previous_proposal_id.number

        request_data = {
                           'sender_uid': ack_message.sender_uid,
                           'proposal_id_sender': ack_message.proposal_id.sender,
                           'proposal_id_number': ack_message.proposal_id.number,
                           'previous_proposal_id_sender': previous_proposal_id_sender,
                           'previous_proposal_id_number': previous_proposal_id_number,
                           'previous_value': ack_message.previous_value
                       }


        result = requests.post(self._instance_url(instance_id) + '/ack_message',data = request_data)

        if result.status_code == 200:
            result = result.json()
            accept_message_json = result['AcceptMessage']
            proposal_id_json = accept_message_json['proposal_id']

            proposal_id = ProposalID(proposal_id_json['sender'], proposal_id_json['number'])
            return AcceptMessage(accept_message_json['sender_uid'], proposal_id, accept_message_json['value'])

    def post_prepare(self, instance_id: str, prepare_message: PrepareMessage) -> AckMessage:
        request_data = {
            'sender_uid': prepare_message.sender_uid,
            'proposal_id_sender': prepare_message.proposal_id.sender,
            'proposal_id_number': prepare_message.proposal_id.number
        }

        result = requests.post(self._instance_url(instance_id) + '/prepare', data=request_data)

        if result.status_code == 200:
            result = result.json()
            ack_message_json = result['AckMessage']
            proposal_id_json = ack_message_json['proposal_id']

            proposal_id = ProposalID(proposal_id_json['sender'], proposal_id_json['number'])

            previous_proposal_id_json = ack_message_json['previous_proposal_id']
            previous_proposal_id = None

            if previous_proposal_id_json is not None:
                previous_proposal_id = ProposalID(previous_proposal_id_json['sender'], previous_proposal_id_json['number'])

            return AckMessage(ack_message_json['sender_uid'], proposal_id, previous_proposal_id, ack_message_json['previous_value'])

    def post_accept(self, instance_id: str, accept_message: AcceptMessage) -> Optional[AckValueMessage]:
        request_data = {
            'sender_uid': accept_message.sender_uid,
            'proposal_id_sender': accept_message.proposal_id.sender,
            'proposal_id_number': accept_message.proposal_id.number,
            'value': accept_message.value
        }

        result = requests.post(self._instance_url(instance_id) + '/accept', data=request_data)

        if result.status_code == 200:
            result = result.json()

            ack_value_message_json = result['AckValueMessage']
            proposal_id_json = ack_value_message_json['proposal_id']

            proposal_id = ProposalID(proposal_id_json['sender'], proposal_id_json['number'])

            return AckValueMessage(ack_value_message_json['sender_uid'], proposal_id)

    def post_accepted(self, instance_id: str, accept_message: AcceptMessage) -> None:
        request_data = {
            'sender_uid': accept_message.sender_uid,
            'proposal_id_sender': accept_message.proposal_id.sender,
            'proposal_id_number': accept_message.proposal_id.number,
            'value': accept_message.value
        }

        requests.post(self._instance_url(instance_id) + '/accepted', data=request_data)

    def _instance_url(self, instance_id):
        return self.base_url + str(instance_id)
