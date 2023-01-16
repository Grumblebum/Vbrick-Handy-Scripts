import requests
import json
from start_recording import start_record
from stop_recording import stop_record

def rev_login():
    url = "https://apitesting.au.vbrickrev.com/api/v1/user/login"
    querystring = {"username": "api.testing", "password": "vbrickrocks"}
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "a1ac4c56-b964-4344-9cfb-8015006e53c3"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    return json.loads(response.text)["token"]


token = rev_login()
videoId = start_record(token)
stop_flag = input("Press Enter/Return when you want to stop!")
stop_record(token, videoId)
