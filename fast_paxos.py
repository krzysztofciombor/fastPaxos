import json
import sys

import requests
from flask import Flask, request, abort  # type: ignore
from flask import render_template
from flask_cors import CORS

from config import BASE_URL

# use embed() to set up interactive endpoint

app = Flask(__name__)
CORS(app)
instances = []


def select_leader():
    return instances[0]  # TODO check heartbeats


def get(url, params=None):
    try:
        return requests.get(url, params, timeout=10)
    except requests.RequestException:
        return None


def post(url, params=None):
    try:
        return requests.post(url, params)
    except requests.ConnectionError:
        return None


@app.route('/')
def home():
    # flip this flag to test on local
    return render_template('home.html', local=json.dumps(False))


@app.route('/heartbeat')
def hello_world():
    return 'Coordinator is working', 200


# API

@app.route('/api/reset', methods=['GET'])
def reset():
    case = request.values.get('case')

    if case == '2':
        for index, instance_url in enumerate(instances):
            if index == 3 or index == 5:
                get(instance_url + '/kill')
            else:
                get(instance_url + '/reset')
    if case == '3':
        for index, instance_url in enumerate(instances):
            if index == 2 or index == 4:
                get(instance_url + '/poison')
            else:
                get(instance_url + '/reset')
    else:
        for instance_url in instances:
            get(instance_url + '/reset')
    prepare_fast()
    return '', 200


@app.route('/api/get_value', methods=['GET'])
def get_value():
    leader = select_leader()
    response = requests.get(leader + '/get_learned_value')
    if response.status_code == 200:
        return response.content, 200
    else:
        abort(404)


def propose_value_classic():
    leader_url = select_leader()
    if not leader_url:
        abort(433)

    # PREPARE LEADER
    post(leader_url + '/propose_value', request.values)
    response = post(leader_url + '/prepare')
    prepare_msg = response.content
    acc_msg = None
    # FIRST PHASE
    for instance_url in instances:
        response = post(instance_url + '/receive_prepare',
                        {"prepare_msg": prepare_msg})
        ack_msg = response.content if response else None
        if ack_msg:
            response = post(leader_url + '/receive_ack',
                            {"ack_msg": ack_msg})
            if response.status_code == 200:
                acc_msg = response.content
    # SECOND PHASE
    if acc_msg:  # TODO: Can we break from the above loop earlier?
        for instance_url in instances:
            response = post(instance_url + '/receive_acc',
                            {"acc_msg": acc_msg})
            ack_value_msg = response.content if response else None
            if ack_value_msg:  # TODO: HACK, every Instance should send this
                # message itself, but it would break threading
                for instance_url2 in instances:
                    post(instance_url2 + '/receive_ack_value',
                         {"ack_value_msg": ack_value_msg})


def propose_value_fast(value):
    for instance_url in instances:
        response = post(instance_url + '/receive_request', {"value": value})
        ack_value_msg = response.content if response else None
        if ack_value_msg:  # TODO: HACK, every Instance should send this
            # message itself, but it would break threading
            for instance_url2 in instances:
                post(instance_url2 + '/receive_ack_value',
                     {"ack_value_msg": ack_value_msg})


@app.route('/api/propose_value', methods=['POST'])
def propose_value_client():
    value = request.values.get('value')
    propose_value_fast(value)
    return '', 200


def prepare_fast():
    leader_url = select_leader()
    response = post(leader_url + '/prepare')
    prepare_msg = response.content
    acc_msg = None
    # FIRST PHASE
    for instance_url in instances:
        response = post(instance_url + '/receive_prepare',
                        {"prepare_msg": prepare_msg})
        ack_msg = response.content if response else None
        if ack_msg:
            response = post(leader_url + '/receive_ack',
                            {"ack_msg": ack_msg})
            if response.status_code == 200:
                acc_msg = response.content
    # SECOND PHASE
    if acc_msg:  # TODO: Can we break from the above loop earlier?
        for instance_url in instances:
            post(instance_url + '/receive_acc',
                 {"acc_msg": acc_msg})


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Specify port and number of instances as arguments")
        sys.exit(1)

    port = int(sys.argv[1])
    instance_count = int(sys.argv[2])

    for x in range(1, instance_count + 1):
        instance_port = port + x
        instances.append("{}:{}".format(BASE_URL, instance_port))

    app.run(debug=True, host='0.0.0.0', processes=10, port=port)
