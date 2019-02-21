# -*- coding: utf-8 -*-

import os
import sys
import json
from service import *
import isodate
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def video_details(client, vid_id):

  response = client.videos().list(
    fields='items(id, snippet/defaultAudioLanguage, snippet/defaultLanguage, snippet/publishedAt, snippet/title, snippet/channelId, snippet/channelTitle, snippet/thumbnails, contentDetails/endAt, statistics)',
    part='snippet,contentDetails,statistics',
    id= vid_id if len(sys.argv) < 2 else sys.argv[1]
  ).execute()

  return response

if __name__ == '__main__':
  client = get_service()
  print video_details(client, 'XbuJ9dxy7qY')
