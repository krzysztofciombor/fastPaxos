import requests

COORDINATOR_NO = 0
BASE_URL = 'http://127.0.0.1:5000/api'

# requests.post(BASE_URL + '/propose_value', {'value': 42})
response = requests.get(BASE_URL + '/get_value')
print(response.content)
