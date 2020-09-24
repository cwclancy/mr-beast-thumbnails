import datetime
import os
import json
import requests
import time
import urllib.request
from PIL import Image, ImageDraw

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload


YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
MR_BEAST_CHANEL_ID = "UCX6OQ3DkcsbYNE6H8uQQuVA"
MR_BEAST_UPLOADS_PLAYLIST_ID = "UUX6OQ3DkcsbYNE6H8uQQuVA"
MR_BEAST_FILE_PATH = "mrbeastmaxres.jpg"
MY_FACE_FILE_PATH = "myface.jpg"
MASK_FILE_PATH = "mask.jpg"
NEW_THUMBNAIL_FILE_PATH = "newthumbnail.jpg"
MY_VIDEO_ID = "JB6Rfxt2wlk"
NUM_SECONDS_PER_DAY = 86400

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "secrets.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, YOUTUBE_SCOPES)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


my_face_img = Image.open(MY_FACE_FILE_PATH)

while True:
    # ask youtube for mr beast uploads info
    playlist_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId="UUX6OQ3DkcsbYNE6H8uQQuVA"
    )
    playlist_response = playlist_request.execute()

    # get best quality thumbnail from most recent video
    most_recent_video_thumbnail_url = playlist_response["items"][0]["snippet"]["thumbnails"]["maxres"]["url"] 
    print(f"got most recent video url: {most_recent_video_thumbnail_url}")

    # save thumbnail to  MR_BEAST_FILE_PATH
    urllib.request.urlretrieve(most_recent_video_thumbnail_url, MR_BEAST_FILE_PATH)

    # open and copy mr beast thumbnail
    mr_beast_thumbnail = Image.open(MR_BEAST_FILE_PATH)
    mr_beast_thumbnail_copy = mr_beast_thumbnail.copy()

    # get premade mask for picture
    face_mask_img = Image.open(MASK_FILE_PATH)

    # copy picture of my face
    my_face_copy = my_face_img.copy()

    # paste my face on mr beast picture and then save to NEW_THUMBNAIL
    mr_beast_thumbnail_copy.paste(my_face_copy, (420, -10), face_mask_img)
    mr_beast_thumbnail_copy.save(NEW_THUMBNAIL_FILE_PATH, quality=95) 

    # update video url
    update_thumbnail_request = youtube.thumbnails().set(
        videoId=MY_VIDEO_ID,
        media_body=MediaFileUpload(NEW_THUMBNAIL_FILE_PATH) # just path to file
    )
    update_thumbnail_response = update_thumbnail_request.execute() 
    print(f"updated thumbnail at {datetime.datetime.now()}")
    time.sleep(NUM_SECONDS_PER_DAY)
    
    




