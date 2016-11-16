BASE_URL = 'http://127.0.0.1'
BASE_PORT = 5000

INTERNAL_API_URL = BASE_URL + ':' + str(BASE_PORT) + '/internal_api'
COORDINATOR_API = BASE_URL + ':' + str(BASE_PORT) + '/coordinator'

INSTANCES = []

for x in range(1, 6):
    instance_port = 5000 + x
    INSTANCES.append("{}:{}".format(BASE_URL, instance_port))
