# -*- coding: utf-8 -*-
# needs to do two things now:
# upload to DDB & update ESS

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
from rest import saveVideoV2
from rest import saveVideoToESS

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

def getLikePercent(likes,dislikes):
  return (likes*100)/(likes+dislikes) if likes > 0 else 80

def getLikePercentStr(likes,dislikes):
  return str(getLikePercent(likes,dislikes)) + '%'

'''
process 1 line from the videos file
'''
def process(client, line):

  video = {}
  tokens = line.split()

  vid_id = tokens[0]
  cat = tokens[1]
  likes = tokens[2]
  dislikes = tokens[3]
  views = tokens[4]
  title = tokens[5]
  pubepoch = tokens[6] # publish date in epoch in secs
  durationInSecs = tokens[7] # duration in secs
  turl = tokens[8]
  vurl = tokens[9]

  # start building video
  video['channel'] = {}
  video['channel']['id'] = vurl
  video['channel']['title'] = 'Hotstar'
  video['channel']['isUserSubscribed'] = False
  video['channel']['newVideosSinceLastVisit'] = False
  video['channel']['lastVisitTime'] = 0
  video['dislikeCount'] = dislikes
  video['duration'] = getHHMMSSTime(durationInSecs)
  video['durationInSeconds'] = durationInSecs
  video['id'] = vid_id
  video['likeCount'] = likes
  video['isLiveStream'] = False
  video['isRestricted'] = False
  video['viewsCountInt'] = views
  video['viewsCount'] = "{:,}".format(views) + ' views'
  video['language'] = 'te'
  video['thumbnailMaxResUrl'] = turl
  video['thumbnailUrl'] = turl
  video['publishDate'] = {}
  video['publishDate']['dateOnly'] = False
  video['publishDate']['tzShift'] = 0
  video['publishDate']['value'] = (pubepoch) * 1000
  video['publishDatePretty'] = getPublishDatePretty(pubepoch)
  video['thumbsUpPercentage'] = getLikePercent(likes,dislikes)
  video['thumbsUpPercentageStr'] = getLikePercentStr(likes,dislikes)
  video['title'] = title

  # stringify
  body_v1 = json.dumps(video) # v1
  body = video  # v2

  # upload the video
  print 'uploading %s to DDB\n' % (vid_id)
  saveVideoV2 (vid_id,cat,title,body['likeCount'],body['viewsCountInt'],body['thumbsUpPercentage'],body['publishDate']['value'],"{}",body)

  print 'uploading %s to ESS\n' % (vid_id)
  saveVideoToESS(cat,vid_id,title,body_v1)

def run():

  client = get_service()

  vid_file = open('/home/akshar/Documents/47mm/hotstar','r')

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
