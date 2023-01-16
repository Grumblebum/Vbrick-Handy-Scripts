import requests
import json
import os
import datetime

# set if to  False if you don`t want to remove file from filesystem
remove_files_after_upload = True
import time

minutes = 5


def authorize():
    # defining the api-endpoint
    API_ENDPOINT_download = "https://apitesting.au.vbrickrev.com/api/v2/user/login"
    # data to be sent to api
    data = {
        "username": "api.testing",
        "password": "sunshine"
    }
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT_download, data=data)
    json_data = json.loads(r.text)
    token = json_data['token']
    headers_download = {
        'Authorization': 'VBrick ' + token
    }

    # defining the api-endpoint
    API_ENDPOINT_upload = "https://random.au.vbrickrev.com/api/v2/user/login"
    # data to be sent to api
    data = {
        "username": "test.user",
        "password": "sunshine"
    }
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT_upload, data=data)
    json_data = json.loads(r.text)
    token = json_data['token']

    headers_upload = {
        'Authorization': 'VBrick ' + token
    }
    return headers_upload, headers_download


headers_upload, headers_download = authorize()


def xstr(s):
    return 'null' if s is None else str(s)


search_url = "https://apitesting.au.vbrickrev.com/api/v2/videos/search"
payload = {'q': '*'}
ids = [x['id'] for x in requests.get(url=search_url, data=payload, headers=headers_download).json()['videos']]

count = 0


def get_id_by_name(name):
    print(name)
    search_url = "https://random.au.vbrickrev.com//api/v2/categories"
    payload = {'name': name}
    cats = requests.get(url=search_url, headers=headers_upload).json()['categories']
    print(cats)
    id_found = [x['categoryId'] for x in cats if x['name'].lower() == name.lower()]
    if id_found:
        return id_found[0]
    else:
        new_cat_id = requests.post(url=search_url, data=payload, headers=headers_upload)
        print(new_cat_id.content)
        new_cat_id = new_cat_id.json()['categoryId']
        return new_cat_id


def get_channel_by_name(name):
    search_url = "https://random.au.vbrickrev.com/api/v2/channels"
    payload = {'name': name}
    channels = requests.get(url=search_url, headers=headers_upload).json()
    print(channels)
    id_found = [x['id'] for x in channels if x['name'].lower() == name.lower()]

    channels_old = requests.get(url="https://apitesting.au.vbrickrev.com/api/v2/channels", headers=headers_download).json()
    print(channels_old)
    role = [x['members'][0]['roleTypes'][0] for x in channels_old if x['name'].lower() == name.lower()][0]
    print(role)
    print(id_found)
    if id_found:
        print('found')
        search_url = "https://random.au.vbrickrev.com/api/v2/channels/{}".format(id_found[0])
        print(search_url)
        payload = {
            "name": name,
            "description": "",
            "members": [
                {
                    "id": "656bde71-db3e-441d-ada5-2eaf7fe44acf",
                    "type": "User",
                    "roleTypes": [
                        role
                    ]
                }
            ]
        }
        print("updated")
        resp = requests.put(url=search_url, json=payload, headers=headers_upload)
        print(resp.content)
        print(resp.status_code)

        return id_found[0]
    else:
        print('not found')

        search_url = "https://random.au.vbrickrev.com/api/v2/channels"
        payload = {
            "name": name,
            "members": [
                {
                    "id": "656bde71-db3e-441d-ada5-2eaf7fe44acf",
                    "type": "User",
                    "roleTypes": [
                        role
                    ]
                }
            ]
        }
        print("updated")
        resp = requests.post(url=search_url, json=payload, headers=headers_upload)
        print(resp.content)
        print(resp.status_code)

        return resp.json()['channelId']


for id in ids:
    if count % 20 == 0 and count != 0:
        print("Paused for 5 min...")
        time.sleep(60 * minutes)
    headers_upload, headers_download = authorize()
    patch = {'op': 'replace', 'path': '/enableDownloads', 'value': 'true'}
    patch_url = "https://apitesting.au.vbrickrev.com/api/v2/videos/{}".format(id)

    patch = requests.patch(url=patch_url, headers=headers_download, data=str(patch))

    search_url = "https://apitesting.au.vbrickrev.com/api/v2/videos/{}/details".format(id)
    print("Downloading metadata for video {}".format(id))
    details = requests.get(url=search_url, headers=headers_download).json()

    print(details)
    if details['categoryPaths']:
        details['categoryIds'] = []
        for index in range(len(details['categoryPaths'])):
            new_id = get_id_by_name(details['categoryPaths'][index]['name'])
            print("New category ID : {}".format(new_id))
            details['categoryPaths'][index]['categoryId'] = new_id
            details['categories'] = []
            details['categories'].append(new_id)
            details['categoryIds'].append(new_id)

    if details['videoAccessControl'] == 'Channels':
        for index in range(len(details['accessControlEntities'])):
            name = details['accessControlEntities'][index]['name']
            new_id = get_channel_by_name(name)
            details['accessControlEntities'][index] = {
                "id": new_id,
                "name": name,
                "type": "Channel",
                "canEdit": 'false'
            }

    inActive = False
    if not details['publishDate'] or details['publishDate'] is None:
        # details['publishDate'] = details['whenUploaded'].split('T')[0]
        inActive = True

    search_url = "https://apitesting.au.vbrickrev.com/api/v2/videos/{}/download".format(id)
    print("Downloading video {}".format(id))
    if not details['linkedUrl']:
        video = requests.get(url=search_url, headers=headers_download).content
    else:
        video = ''

    print("Downloaded")
    temp = ''
    for i in details.keys():
        if i not in ['id', 'title', 'uploader', 'thumbnailUrl', 'customFields', 'userTags']:
            if i in ['htmlDescription', 'description', 'linkedUrl', 'categoryIds', 'isActive', 'approvalStatus',
                     'password', 'tags', 'enableComments', 'accessControlEntities',
                     'enableRatings', 'enableDownloads', 'status', 'canEdit', 'videoAccessControl',
                     'whenUploaded', 'lastViewed', 'sourceType', 'expirationDate', 'expirationAction', 'publishDate',
                     'is360', 'unlisted', 'totalViews', 'overallProgress', 'ifsProcessing']:
                temp += ('" , "' + i + '": "' + xstr(details[i]))

    payload = {'Video': '{"title": "' + details['title'] + temp + '" , "uploader": "test.user", }'}
    files = {
        'file': (os.path.join(id, 'video.mp4'), video, 'video/mp4'),
    }
    payload['Video'] = payload['Video'].replace('"[', '[').replace(']"', ']').replace('"null"', 'null')
    if not details['linkedUrl']:
        try:
            count += 1
            new_id = requests.post(url="https://random.au.vbrickrev.com/api/uploads/videos", data=payload, files=files,
                                   headers=headers_upload)
            print(new_id)
            print(new_id.content)

            new_id = new_id.json()['videoId']
        except Exception as e:
            print(str(e))
            continue
        if inActive:
            pass
    else:
        print("Live video uploading")
        playback = {}
        for i in details.keys():
            if i not in ['id', 'uploader', 'thumbnailUrl', 'customFields', 'userTags']:
                if i in ['title', 'description', 'linkedUrl', 'categoryIds', 'isActive',
                         'password', 'tags', 'enableComments', 'accessControlEntities',
                         'enableRatings', 'enableDownloads',  'canEdit', 'videoAccessControl', 'publishDate']:
                    playback[i] = details[i]
        playback['uploader'] = 'test.user'
        print(playback)

        new_id = requests.post(url="https://random.au.vbrickrev.com/api/v2/videos", json=playback,
                               headers=headers_upload)
        print(new_id)
        print(new_id.content)


    print("Video uploaded")
    if details['thumbnailUrl']:
        thumb_url = 'https://random.au.vbrickrev.com/api/uploads/images/{}'.format(new_id)
        thumb = requests.get(details['thumbnailUrl']).content
        files = {
            'file': (os.path.join(id, 'thumbnail.jpg'), thumb, 'image/jpeg'),
        }
        new_id = requests.post(url=thumb_url, files=files, headers=headers_upload)
        print("thumbnail uploaded")
