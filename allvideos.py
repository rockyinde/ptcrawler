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
    #print(response)
    print_playlists(response)

    request = client.playlists().list_next(
      request, response)
    '''
    request = client.playlists().list(
                #part='snippet,contentDetails',
                part='id,snippet',
                fields='items(snippet/title,id)',
                channelId='UC_x5XG1OV2P6uZZ5FSM9Ttw' if len(sys.argv) < 2 else sys.argv[1],
                maxResults=5,
                pageToken=response.nextPageToken
              ) if response.nextPageToken else None
              '''

def get_uploads_playlist_id():
  # Retrieve the contentDetails part of the channel resource for the
  # authenticated user's channel.
  channels_response = youtube.channels().list(
    id='UC_x5XG1OV2P6uZZ5FSM9Ttw' if len(sys.argv) < 2 else sys.argv[1],
    #id=UCYSr1LyiArqdc_z9nJoCHXw
    part='contentDetails'
  ).execute()

  for channel in channels_response['items']:
    # From the API response, extract the playlist ID that identifies the list
    # of videos uploaded to the authenticated user's channel.
    return channel['contentDetails']['relatedPlaylists']['uploads']

  return None

def list_uploaded_videos(uploads_playlist_id):
  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_playlist_id,
    part='snippet,contentDetails',
    fields='items(id, snippet/title, snippet/resourceId/videoId, contentDetails/endAt)',
    maxResults=25
  )

  print 'Videos in list %s' % uploads_playlist_id
  while playlistitems_list_request:
    time.sleep(1)
    playlistitems_list_response = playlistitems_list_request.execute()

    # Print information about each video.
    for playlist_item in playlistitems_list_response['items']:
      title = playlist_item['snippet']['title']
      video_id = playlist_item['snippet']['resourceId']['videoId']
      print '%s (%s)' % (title, video_id)
      print playlist_item

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

