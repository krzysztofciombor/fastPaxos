from flask import Flask, jsonify, abort, request  # type: ignore
from src.Instance import Instance
from src.Paxos import get_classic_quorum_size
from src.ProposalID import ProposalID
from IPython import embed  # type: ignore
from src.Message import AckMessage, PrepareMessage, AcceptMessage
from src.HttpClient import HttpClient

# use embed() to set up interactive endpoint

app = Flask(__name__)

number_of_instances = 5
quorum_size = get_classic_quorum_size(number_of_instances)
instances = []

for x in range(number_of_instances):
    instances.append(Instance(str(x), quorum_size))

@app.route('/heartbeat')
def hello_world():
    return 'Hello World!'

@app.route('/internal_api/instances/<int:instance_id>/heartbeat', methods=['GET'])
def instance_hearbeat(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]
        return jsonify({'alive': instance.get_active()})
    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/prepare', methods=['GET'])
def prepare(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]
        result = instance.prepare()
        return jsonify(
            {
                'PrepareMessage': {
                    'sender_uid': result.sender_uid,
                    'proposal_id': {
                        'sender': result.proposal_id.sender,
                        'number': result.proposal_id.number
                    }
                }
            }
        )
    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/value', methods=['POST'])
def propose_value(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]
        value = request.values.get('value')
        instance.propose_value(value)
        return '', 202
    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/ack_message', methods=['POST'])
def receive_ack_message(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]

        sender_uid = request.values.get('sender_uid')
        proposal_id_sender = request.values.get('proposal_id_sender')
        proposal_id_number = request.values.get('proposal_id_number')
        previous_proposal_id_sender = request.values.get('previous_proposal_id_sender')
        previous_proposal_id_number = request.values.get('previous_proposal_id_number')
        previous_value = request.values.get('previous_value')

        proposal_id = ProposalID(proposal_id_sender, proposal_id_number)
        previous_proposal_id = None
        if previous_proposal_id_number is not None and previous_proposal_id_sender is not None:
            previous_proposal_id = ProposalID(previous_proposal_id_sender, previous_proposal_id_number)

        ack_message = AckMessage(sender_uid, proposal_id, previous_proposal_id, previous_value)

        result = instance.receive_ack_message(ack_message)

        if result is not None:
            return jsonify(
                {
                    'AcceptMessage': {
                        'sender_uid': result.sender_uid,
                        'proposal_id': {
                            'sender': result.proposal_id.sender,
                            'number': result.proposal_id.number
                        },
                        'value': result.value
                    }
                }
            )
        else:
            return '', 202
    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/prepare', methods=['POST'])
def receive_prepare(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]

        sender_uid = request.values.get('sender_uid')
        proposal_id_sender = request.values.get('proposal_id_sender')
        proposal_id_number = request.values.get('proposal_id_number')

        proposal_id = ProposalID(proposal_id_sender, proposal_id_number)
        prepare_message = PrepareMessage(sender_uid, proposal_id)
        result = instance.receive_prepare(prepare_message)

        result_previous_proposal_id = result.previous_proposal_id

        result_previous_proposal_id_dict = None
        if result_previous_proposal_id is not None:
            result_previous_proposal_id_dict = {
                'sender': result_previous_proposal_id.sender,
                'number': result_previous_proposal_id.number
            }

        return jsonify(
            {
                'AckMessage': {
                    'sender_uid': result.sender_uid,
                    'proposal_id': {
                        'sender': result.proposal_id.sender,
                        'number': result.proposal_id.number
                    },
                    'previous_proposal_id': result_previous_proposal_id_dict,
                    'previous_value': result.previous_value
                }
            }
        )

    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/accept', methods=['POST'])
def receive_accept(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]

        sender_uid = request.values.get('sender_uid')
        proposal_id_sender = request.values.get('proposal_id_sender')
        proposal_id_number = request.values.get('proposal_id_number')
        value = request.values.get('value')

        proposal_id = ProposalID(proposal_id_sender, proposal_id_number)

        accept_message = AcceptMessage(sender_uid, proposal_id, value)
        result = instance.receive_accept(accept_message)

        if result is not None:
            return jsonify(
                {
                    'AckValueMessage': {
                        'sender_uid': result.sender_uid,
                        'proposal_id': {
                            'sender': result.proposal_id.sender,
                            'number': result.proposal_id.number
                        }
                    }
                }
            )
        else:
            return '', 202
    else:
        abort(404)

@app.route('/internal_api/instances/<int:instance_id>/accepted', methods=['POST'])
def receive_accepted(instance_id):
    if instance_id < len(instances):
        instance = instances[instance_id]
        sender_uid = request.values.get('sender_uid')
        proposal_id_sender = request.values.get('proposal_id_sender')
        proposal_id_number = request.values.get('proposal_id_number')
        value = request.values.get('value')

        proposal_id = ProposalID(proposal_id_sender, proposal_id_number)

        accept_message = AcceptMessage(sender_uid, proposal_id, value)
        instance.receive_accepted(accept_message)

        return '', 202
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', processes=10)
