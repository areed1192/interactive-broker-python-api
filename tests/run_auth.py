import requests
from pprint import pprint
    
# Create a new session.
new_session = requests.Session()
new_session.verify = False

new_request: requests.PreparedRequest = requests.Request(
    method='GET',
    url=r'https://localhost:5000/v1/portal/iserver/auth/status',
    headers=None,
    params=None,
    data=None,
    json=None
).prepare()

print(new_request.path_url)
print(new_request.headers)
response: requests.Response = new_session.send(new_request)


# url = 'https://localhost:5000/v1/portal/iserver/auth/status'
# response = requests.post(url=url, verify=False, params=None, json=None, data=None)
# print(response.status_code)

pprint(response.text)