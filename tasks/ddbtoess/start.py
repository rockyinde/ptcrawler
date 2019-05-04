# -*- coding: utf-8 -*-

import os
import json

from rest import fetchVideo
from rest import postVideoToESS

def scan():
  
  cats = ['r','h','c','p','o']

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
        r = postVideoToESS(items[i])
        print 'response from ESS: %s\n' % (r.content)

      # fetch next page
      if not ('LastEvaluatedKey' in resp):
        print 'no more pages for this cat\n'
        cont = False
      else:
        pt = resp['LastEvaluatedKey']

if __name__ == '__main__':
  scan()
  #print getHHMMSSTime('PT2H12M40S')
  #print getPublishDatePretty('2019-01-05T09:29:54.000Z')
  #print getLikePercent(10,4)
