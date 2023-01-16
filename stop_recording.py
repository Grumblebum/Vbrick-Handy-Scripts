import requests
import json


def stop_record(token, videoId):
    url = "https://apitesting.au.vbrickrev.com/api/v1/vc/stop-recording"
    querystring = {"videoId": "{}".format(videoId)}
    headers = {
        'Authorization': "VBrick {}".format(token),
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "b52a4a22-fd5e-4d77-bce4-c56f58572b1b"
    }
    response = requests.request("POST", url, headers=headers, params=querystring)
    print(response.text)