# -------------------------
# YTV_Search.py
# -------------------------
# Language Python 
# Ver. 1.0
# Date 20-03-2023
# Author Riccardo Raggi
# ---------------------------------------------------------------------
# Searching a group of videos, collect the videos into a CSV File
# ---------------------------------------------------------------------
# CSV Record
#
# Video, YTV Title, YTV Link, YTV ID, YTV Published Date, YTV Channel
# ---------------------------------------------------------------------
#
# LIBRARIES
#
import os
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import art
import re
import tkinter as tk
try:
    from re import *
    from art import *
    from tkinter import simpledialog
except ModuleNotFoundError:
    os.system('pip install urllib.request')
    os.system('pip install art')
#
# API information
#
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = '<YOUTUBE_DEVELOPER_KEY>'       # Replacing <YOUTUBE_DEVELOPER_KEY> with your Youtube Key
#
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
#
# Dictionary to store videos data in CSV
Video_info = {
    'Video':[],
    'Title':[],
    'YTV_Link':[],
    'YTV_Id':[],
    'Published':[],
    'Channel':[]
}
#
# FUNCTIONS
#
def channel(chnId):
    chn_req = youtube.channels().list(
        part = "snippet",
        id = chnId )
    chn_resp = chn_req.execute()
    for item in chn_resp['items']:
        chn_title = item['snippet']['title']
        return chn_title       
#
# BANNER
#
tprint("Youtube")
tprint("Video link + Title")
print("Developed By Riccardo R - Google API")
print("------------------------------------")
#
# Input box
#       
Box = tk.Tk()
Box.withdraw()
# the input dialog
Video = simpledialog.askstring(title="YTV Searching", prompt="What Video ?:")
qVideo = chr(34) + Video + chr(34)
#
data = []
pageToken = ""
while True:
    res = youtube.search().list(
        q=qVideo,
        part='snippet',
        type='video',
        maxResults=50,
        order="date",
        publishedAfter="2010-01-01T00:00:00Z",                  # If you want to get a video after a particular date
        pageToken=pageToken if pageToken != "" else ""
    ).execute()
    v = res.get('items', [])
    if v:
        data.extend(v)
    pageToken = res.get('nextPageToken')
    if not pageToken:
        break
#
# CSV file - Extracting & Writing
#
for item in data:
    # Getting the id
    vidId = item['id']['videoId']
    Title = item['snippet']['title']
    Published = item['snippet']['publishedAt']
    chnId = item['snippet']['channelId']
    
    chn_title = channel(chnId)
    
    Video_info['Video'].append(Video)
    Video_info['Title'].append(Title)
    Dummy = "https://youtu.be/" + vidId
    Video_info['YTV_Link'].append(Dummy)
    Video_info['YTV_Id'].append(vidId)
    Video_info['Published'].append(Published)
    Video_info['Channel'].append(chn_title)
    
#
CsvFile = Video + ".csv"
pd.DataFrame(data=Video_info).to_csv(CsvFile, index=False)

print()
print(len(data), "Lines written")