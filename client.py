import argparse

import requests

COORDINATOR_NO = 0
BASE_URL = 'http://127.0.0.1:5000/api'


def main(value=None):
    if value:
        requests.post(BASE_URL + '/propose_value', {'value': value})
    else:
        response = requests.get(BASE_URL + '/get_value')
        print(response.content)


def reset():
    requests.get(BASE_URL + '/reset')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--value')
    parser.add_argument('-r', action='store_true')
    args = parser.parse_args()
    if args.r:
        reset()
    else:
        main(args.value)
