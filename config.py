BASE_URL = 'http://127.0.0.1'
BASE_PORT = 5000

INTERNAL_API_URL = BASE_URL + ':' + str(BASE_PORT) + '/internal_api'
COORDINATOR_API = BASE_URL + ':' + str(BASE_PORT) + '/coordinator'

INSTANCES = [
    BASE_URL + ':5001',
    BASE_URL + ':5002',
]
