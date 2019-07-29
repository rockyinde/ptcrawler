# -*- coding: utf-8 -*-

import os
import json
import time

from rest import fetchVideo
from rest import postVideoToESS
from rest import saveVideoV2

# validates whether the item has all the attributes needed for V2
def is_valid (item):

  # empty check
  if not item or not 'body' in item or not 'cat' in item:
    return False

  try:
    body = json.loads(item['body'])
  except TypeError, e:
    print 'error %s\n' % (e)
    return False

  # channel info
  if not 'channel' in body or not 'id' in body['channel'] or not 'title' in body['channel']:
    print 'no channel found in video'
    return False

  # base keys
  basekeys = ['likeCount','viewsCountInt','thumbsUpPercentage']
  for key in basekeys:
    if not key in body:
      print 'key %s not found\n' % (key)
      return False

  # pdate
  if not 'publishDate' in body or not 'value' in body['publishDate']:
    print 'publish date not found\n'
    return False

  return True

def scan():
  
  #cats = ['r','h','c','p','o']
  cats = ['o']

  # for each category
  for cat in cats:
    print 'Now starting cat: %s\n' % (cat)
    cont = True
    pt = None

    while(cont):
      resp = fetchVideo(cat, pt)
      count = resp['Count']
      items = resp['Items']

      print 'Processing response with video count: %s\n' % (count)
      for i in range(count):

        # fetch item
        item = items[i]
        if not is_valid(item):
          print 'failed for %s' % (json.dumps(item))
          continue

        body = json.loads(item['body'])

        # save to V2
        respV2 = saveVideoV2 (item['id'],item['cat'],item['title'],body['likeCount'],body['viewsCountInt'],body['thumbsUpPercentage'],body['publishDate']['value'],"{}",body)
        print 'response from AWS: %s\n' % (respV2.content)

      time.sleep(1)

      # fetch next page
      if not ('LastEvaluatedKey' in resp):
        print 'no more pages for this cat\n'
        cont = False
      else:
        pt = resp['LastEvaluatedKey']

    time.sleep(1)

if __name__ == '__main__':
  scan()
  #print getHHMMSSTime('PT2H12M40S')
  #print getPublishDatePretty('2019-01-05T09:29:54.000Z')
  #print getLikePercent(10,4)
