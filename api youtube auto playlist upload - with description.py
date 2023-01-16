from __future__ import unicode_literals
import requests
import json
import glob
import youtube_dl
import os

dirpath = os.getcwd()

ydl_opts = {
    'format': 'mp4',
    'writedescription' : True
}

original_fileurl = ''
fname = ''
url = 'https://www.youtube.com/watch?v=OCF265HXAPw&list=PLMo7gORxrRhXoy5vRjdE5JdqSMtlqlx_f'
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
    ydl_info = ydl.extract_info(url, download=False)
    # info = ydl.extract_info('https://www.youtube.com/watch?v=SBhGY02ZlMQ', download=False)
    # filename = ydl.prepare_filename(info)
    # original_filename = filename.split('-')[0]+'.mp4'
    # fname = filename.split('-')[0]
    # original_fileurl = os.path.join(dirpath,filename)


# defining the api-endpoint
API_ENDPOINT = "https://random.au.vbrickrev.com/api/v2/user/login"

# data to be sent to api
data = {
    "username": "test.user",
    "password": "sunshine"
}

r = requests.post(url=API_ENDPOINT, data=data)

json_data = json.loads(r.text)
token = json_data['token']

headers = {
    'Authorization': 'VBrick ' + token
}


API_ENDPOINT_FOR_UPLOAD = "https://random.au.vbrickrev.com/api/uploads/videos"

flist = []
for filename in glob.glob('*.mp4'):
    f = open(filename.replace('.mp4', '.description'), "r")
    description = f.read()
    f.close()
    original_fileurl = os.path.join(dirpath, filename)
    flist.append(original_fileurl)
    flist.append(original_fileurl.replace('.mp4', '.description'))
    flist.append(original_fileurl.replace('.mp4', '.txt'))

    title = filename.split(' -')[0]+'.mp4'
    payload = {'Video': '{"title": "' + filename[:-16] + '" , "description": "' + description + '" , "uploader": "test.user", }'}
    files = {
        'file': (filename.split(' -')[0]+'.mp4', open(original_fileurl, 'rb'), 'video/mp4'),
    }
    print(files)
    res = requests.post(url=API_ENDPOINT_FOR_UPLOAD, data=payload, files=files, headers=headers)

    print(res)
    print(res.text)

for val in flist:
    try:
        os.remove(val)
    except Exception:
        pass # if you do not want to remove the files from your computer, then make this paramter inactive using "#"
