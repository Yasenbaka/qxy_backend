import json

import requests

response = requests.get('http://127.0.0.1:8000/api/name?name=你好').text
response = json.loads(response)
print(response['message'])
