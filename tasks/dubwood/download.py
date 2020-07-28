#!/usr/bin/python

import argparse
import os
import re
import time
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from service import *

DEVELOPER_KEY = "AIzaSyCKfhAgUThXhv7r6k0XKCyk3r3ckO9-7G4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# etvcinema = UC3Dvbf4eEov7YORy5nEioTA
# mallemalatv = UCULLmfWqhMOeiWEV6hkMSCg

playlist_filter_negative = ["song","promo","scene","show","launch","serial","event","live","private","part","update","success","celebrations","interview","gossip","news","press","media","teaser","trailer"]
playlist_filter_positive = []

vids_file = open('/home/akshar/Documents/dubwood/videos','w')

'''
filter whether or not to pass a playlist 
for further processing
'''
def filter (text):
    for pos in playlist_filter_positive:
        if pos in text.lower():
            return True
    for neg in playlist_filter_negative:
        if neg in text.lower():
            return False

    return True

'''
filter whether or not to pass a title
for further processing
'''
def filterTitle (text):
    for neg in playlist_filter_negative:
        if neg in text.lower():
            return False

    return True

'''
browse all the playlists of the given channel
paginates the requests
'''
def playlists_list_by_channel_id(client):

  # build the request
  request = client.playlists().list(
                #part='snippet,contentDetails',
                part='id,snippet',
                fields='items(snippet/title,id),nextPageToken',
                channelId='UC_x5XG1OV2P6uZZ5FSM9Ttw' if len(sys.argv) < 2 else sys.argv[1],
                maxResults=5
              )

  # iterate through each page
  while request:
    time.sleep(1)

    response = request.execute()
    #print_playlists(response)

    request = client.playlists().list_next(
      request, response)
    for playlist in response['items']:
      if filter(playlist['snippet']['title']):
          print 'pass %s (%s)' % (playlist['snippet']['title'], playlist['id'])
          print '*****************now printing playlist*****************'
          list_playlist_videos(playlist['id'])

def video_duration(client, vid_id):

  response = client.videos().list(
    fields='items(contentDetails/duration)',
    part='contentDetails',
    id=vid_id
  ).execute()

  try:
    secs = getDurationInSecs(response['items'][0]['contentDetails']['duration'])
  except:
    print 'error'
    secs = 0

  return secs

def is_movie_duration(client, vid_id):
  duration = video_duration(client, vid_id)
  return duration > 5400  # 1.5 HOUR

'''
crawls the list of videos in the playlist
and enumerates suitable matches
'''
def list_playlist_videos(playlist_id):
  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=playlist_id,
    part='snippet,contentDetails',
    fields='items(id, snippet/title, snippet/resourceId/videoId, contentDetails/endAt),nextPageToken',
    maxResults=25
  )

  print 'Videos in list %s' % playlist_id
  while playlistitems_list_request:
    time.sleep(1)
    playlistitems_list_response = playlistitems_list_request.execute()

    # Print information about each video.
    for playlist_item in playlistitems_list_response['items']:
      title = playlist_item['snippet']['title']
      if not filterTitle(title):
        continue
      time.sleep(1)
      video_id = playlist_item['snippet']['resourceId']['videoId']
      if not is_movie_duration(youtube, video_id):
        continue
      print '%s (%s)' % (title, video_id)
      vids_file.write('%s %s \n' % (video_id, title.encode('ascii', 'ignore').decode('ascii')))

    playlistitems_list_request = youtube.playlistItems().list_next(
      playlistitems_list_request, playlistitems_list_response)

if __name__ == '__main__':
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  try:
    #uploads_playlist_id = get_uploads_playlist_id()
    #if uploads_playlist_id:
     # list_uploaded_videos(uploads_playlist_id)
    #else:
     # print('There is no uploaded videos playlist for this user.')
    playlists_list_by_channel_id(youtube)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)

