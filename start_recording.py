import requests
import json

def start_record(token):
    url = "https://apitesting.au.vbrickrev.com/api/v1/vc/start-recording"
    querystring = {"title": "Morning Call Recording", "sipAddress": "[insert sip address]"}
    headers = {
        'Authorization': "VBrick {}".format(token),
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "[insert token]"
    }
    response = requests.request("POST", url, headers=headers, params=querystring)
    print(response.text)
    return json.loads(response.text)["videoId"]