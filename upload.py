# -*- coding: utf-8 -*-

import os
import json
from service import *
import isodate
import datetime
import dateutil.parser
import calendar
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rest import saveVideo

def getDurationInSecs(time):
  duration = isodate.parse_duration(time)
  return int(duration.total_seconds())

def getHHMMSSTime(time):
  return str(datetime.timedelta(seconds=getDurationInSecs(time)))

def getEpochFromStr(timestamp):
  dt = dateutil.parser.parse(timestamp)
  return calendar.timegm(dt.timetuple())

def getPublishDatePretty(timestamp):
  dt = dateutil.parser.parse(timestamp)
  now = pytz.utc.localize(datetime.datetime.now())

  return str((now - dt).days/365) + ' years ago'

def video_details(client, vid_id):

  response = client.videos().list(
    fields='items(id, snippet/defaultAudioLanguage, snippet/defaultLanguage, snippet/publishedAt, snippet/title, snippet/channelId, snippet/channelTitle, snippet/thumbnails, contentDetails/duration, statistics)',
    part='snippet,contentDetails,statistics',
    id=vid_id
  ).execute()

  return response

def getLikePercent(likes,dislikes):
  return likes*100/(likes+dislikes)

def getLikePercentStr(likes,dislikes):
  return str(likes*100/(likes+dislikes)) + '%'

'''
process 1 line from the videos file
'''
def process(client, line):

  video = {}
  tokens = line.split()
  cat = tokens[0]
  vid_id = tokens[1]

  details=video_details(client,vid_id)

  item = details['items'][0]
  # statistics n/a for all videos
  likes = int(item['statistics']['likeCount']) if 'likeCount' in item['statistics'] else 80 
  dislikes = int(item['statistics']['dislikeCount']) if 'dislikeCount' in item['statistics'] else 20
  title = item['snippet']['title']

  # start building video
  video['channel'] = {}
  video['channel']['id'] = item['snippet']['channelId']
  video['channel']['title'] = item['snippet']['channelTitle']
  video['channel']['isUserSubscribed'] = False
  video['channel']['newVideosSinceLastVisit'] = False
  video['channel']['lastVisitTime'] = 0
  video['dislikeCount'] = dislikes
  video['duration'] = getHHMMSSTime(item['contentDetails']['duration'])
  video['durationInSeconds'] = getDurationInSecs(item['contentDetails']['duration'])
  video['id'] = item['id']
  video['likeCount'] = likes
  video['isLiveStream'] = False
  video['isRestricted'] = False
  video['language'] = 'te'
  video['viewsCountInt'] = int(item['statistics']['viewCount'])
  video['viewsCount'] = "{:,}".format(int(item['statistics']['viewCount'])) + ' views'
  video['language'] = 'te'
  video['thumbnailMaxResUrl'] = item['snippet']['thumbnails']['maxres']['url'] if 'maxres' in item['snippet']['thumbnails'] else item['snippet']['thumbnails']['default']['url']
  video['thumbnailUrl'] = item['snippet']['thumbnails']['high']['url']
  video['publishDate'] = {}
  video['publishDate']['dateOnly'] = False
  video['publishDate']['tzShift'] = 0
  video['publishDate']['value'] = getEpochFromStr(item['snippet']['publishedAt']) * 1000
  video['publishDatePretty'] = getPublishDatePretty(item['snippet']['publishedAt'])
  video['thumbsUpPercentage'] = getLikePercent(likes,dislikes)
  video['thumbsUpPercentageStr'] = getLikePercentStr(likes,dislikes)
  video['title'] = item['snippet']['title']

  # stringify
  body = json.dumps(video)

  # upload the video
  print 'uploading %s\n' % (vid_id)
  saveVideo(cat,vid_id,title,body)

def run():

  client = get_service()

  vid_file = open('/tmp/videos','r')

  line = vid_file.readline()
  while line:
      try:
          process(client, line)
          line = vid_file.readline()
      except HttpError, e:
          print 'exception when handline movie %s\n' % (line)
          print 'error: %s\n' % (e.content)
  

if __name__ == '__main__':
  run()
  #print getHHMMSSTime('PT2H12M40S')
  #print getPublishDatePretty('2019-01-05T09:29:54.000Z')
  #print getLikePercent(10,4)
