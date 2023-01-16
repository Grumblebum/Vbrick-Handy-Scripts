from __future__ import unicode_literals
import requests
import json
import glob
import youtube_dl
import os

dirpath = os.getcwd()

ydl_opts = {
    'format': 'mp4'
}

original_fileurl = ''
fname = ''

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=SBhGY02ZlMQ'])
    # info = ydl.extract_info('https://www.youtube.com/watch?v=SBhGY02ZlMQ', download=False)
    # filename = ydl.prepare_filename(info)
    # original_filename = filename.split('-')[0]+'.mp4'
    # fname = filename.split('-')[0]
    # original_fileurl = os.path.join(dirpath,filename)


# defining the api-endpoint
API_ENDPOINT = "https://apitesting.au.vbrickrev.com/api/v1/user/login"

# data to be sent to api
data = {
    "username": "test.user",
    "password": "sunshine"
}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

json_data = json.loads(r.text)
token = json_data['token']

headers = {
    'Authorization': 'VBrick ' + token
}


API_ENDPOINT_FOR_UPLOAD = "https://apitesting.au.vbrickrev.com/api/uploads/videos"

flist = []
for filename in glob.glob('*.mp4'):
    original_fileurl = os.path.join(dirpath, filename)
    flist.append(original_fileurl)
    title = filename.split(' -')[0]+'.mp4'
    payload = {'Video': '{"title": "' + filename[:-16] + '" ,"uploader": "test.user"}'}
    files = {
        'file': (filename.split(' -')[0]+'.mp4', open(original_fileurl, 'rb'), 'video/mp4'),
    }
    print(files)
    res = requests.post(url=API_ENDPOINT_FOR_UPLOAD, data=payload, files=files, headers=headers)

    print(res)
    print(res.text)

for val in flist:
    os.remove(
        val)  # if you do not want to remove the files from your computer, then make this paramter inactive using "#"
