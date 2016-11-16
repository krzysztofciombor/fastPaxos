import requests
from flask import Flask, request, abort  # type: ignore

from config import INSTANCES

# use embed() to set up interactive endpoint

app = Flask(__name__)

LEADER_URL = INSTANCES[0]


@app.route('/heartbeat')
def hello_world():
    return 'Hello World!'


@app.route('/api/get_value', methods=['GET'])
def get_value():
    response = requests.get(LEADER_URL + '/get_learned_value')
    if response.status_code == 200:
        return response.content, 200
    else:
        abort(404)


@app.route('/api/propose_value', methods=['POST'])
def propose_value_client():
    requests.post(LEADER_URL + '/propose_value', request.values)
    response = requests.post(LEADER_URL + '/prepare')
    prepare_msg = response.content
    acc_msg = None
    # FIRST PHASE
    for instance_url in INSTANCES:
        response = requests.post(instance_url + '/receive_prepare',
                                 {"prepare_msg": prepare_msg})
        ack_msg = response.content
        if ack_msg:
            response = requests.post(LEADER_URL + '/receive_ack',
                                     {"ack_msg": ack_msg})
            if response.status_code == 200:
                acc_msg = response.content
    # SECOND PHASE
    if acc_msg:  # TODO: Can we break from the above loop earlier?
        for instance_url in INSTANCES:
            ack_value_msg = requests.post(instance_url + '/receive_acc',
                                          {"acc_msg": acc_msg}).content
            if ack_value_msg:  # TODO: HACK, every Instance should send this message itself, but it would break threading
                for instance_url2 in INSTANCES:
                    requests.post(instance_url2 + '/receive_ack_value',
                                  {"ack_value_msg": ack_value_msg})

    return '', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', processes=10)
