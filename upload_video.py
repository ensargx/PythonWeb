import json
import os
import re
from dotenv import load_dotenv
import requests
import time

# Load environment variables
load_dotenv()


def get_access_token():
    # Get access token from a refresh token
    # Return a tuple of (access_token, expires_in)
    refresh_token = os.getenv('REFRESH_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    })
    print(f"Getting access token: {r.status_code}")
    if not r.status_code == 200:
        print("Failed to get access token!")
        print(r.content)
    # print(r.json())
    return r.json()['access_token'], r.json()['expires_in']

def load_videos(path):
    # Load videos from a path
    # Return a list of videos
    videos = []
    with open(path, 'r') as f:
        contents = f.read()
    videos = json.loads(contents)
    return videos

def download_video(title, url):
    # Download a video from a url
    # Return a video object
    os.system(f"curl '{url}' -o '{title}.mp4'")

def check_if_auth_code_valid(auth_code):
    r = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=Ks-_Mh1QhMc&key={auth_code}')
    print(f"Checking if auth code is valid: {r.status_code}")
    if not r.status_code == 200:
        print("Auth code is not valid!")
        print(r.content)
    assert r.status_code == 200

def get_download_link(video_id):
    main_url = f'https://video.sibnet.ru/shell.php?videoid={video_id}'
    r = requests.get(main_url)
    assert r.status_code == 200

    url = re.search(b"src: \"(.*)\", type: \"video/mp4\"", r.content).group(1).decode()
    url = f"https://video.sibnet.ru{url}"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    r = requests.head(url, headers={'Referer': main_url, 'User-Agent': user_agent}, allow_redirects=False)
    if not r.status_code == 302:
        print("Failed to get download link!")
        print(r.headers)
        print(r.content)
    url = r.headers.get('Location')[2:]
    url = f"https://{url}"

    r = requests.get(url, headers={'User-Agent': user_agent}, allow_redirects=False)
    url = r.headers.get('Location')
    print(f"Getting download link: {r.status_code}")
    return url

def create_resumable_upload(auth_token, video_len, title):
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,contentDetails", headers={
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Upload-Content-Length': video_len,
        'X-Upload-Content-Type': 'video/mp4'
    }, json={
        'snippet': {
            'title': title,
            'description': 'Uploaded from Python'
        },
        'status': {
            'privacyStatus': 'private'
        }
    })
    print(f"Creating resumable upload: {r.status_code}")
    if not r.status_code == 200:
        print("Failed to create resumable upload!")
        print(r.content)
    # print(r.headers)
    return r.headers['Location']

def upload_video(location, title, auth_token, video_len):
    print(f"Uploading video: {title}")
    video_bin = open(f'{title}.mp4', 'rb').read()
    print(f"Video length: {video_len}")
    r = requests.put(location, data=video_bin, headers={
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'video/mp4',
        'Content-Length': video_len
    })
    print(r.status_code)

auth_token = os.getenv('AUTH_TOKEN')
assert auth_token != None
# check_if_auth_code_valid(auth_token)
videos = load_videos('videos.json')

time_now = time.time()
auth_token, expires_in = get_access_token()

for video in videos:
    if time.time() - time_now > expires_in:
        auth_token, expires_in = get_access_token()
    title = video['title']
    video_id = int(video['id'])
    url = get_download_link(video_id)
    download_video(title, url)
    video_len = str(os.path.getsize(f'{title}.mp4'))
    location = create_resumable_upload(auth_token, video_len, title)
    upload_video(location, title, auth_token, video_len)
