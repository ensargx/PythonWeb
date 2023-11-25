import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

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

    print(r.status_code)
    print(r.headers)
    return r.headers['Location']

def upload_video(location, title, auth_token, video_len):
    video_bin = open(f'{title}.mp4', 'rb').read()
    r = requests.put(location, data=video_bin, headers={
        'Authorization:': f'Bearer {auth_token}',
        'Content-Type': 'video/mp4',
        'Content-Length': video_len
    })


auth_token = os.getenv('AUTH_TOKEN')
videos = load_videos('videos.json')

for video in videos:
    title = video['title']
    url = video['url']
    download_video(title, url)
    video_len = str(os.path.getsize(f'{title}.mp4'))
    location = create_resumable_upload(auth_token, video_len, title)
    upload_video(location, title, auth_token, video_len)
