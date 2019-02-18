# -*- coding: utf-8 -*-

import os
from dateutil.parser import parse

from googleapiclient.discovery import build

DEVELOPER_KEY = "AIzaSyCKfhAgUThXhv7r6k0XKCyk3r3ckO9-7G4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_service():
   return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def print_response(response):
  print(response)

def print_playlists (response):

  for playlist in response['items']:
      print '%s' % (playlist['snippet']['title'])

def parseYear (text):
  try:
    return parse(text, fuzzy=True).year
  except ValueError, e:
    return None

