import requests
import json

url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/save'
fetch_url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/videos'

# change the type of the document if using for a different appication
ess_url = 'https://search-tmovies-h6qlkaunfxq6rrnd7fqoot7cuu.ap-south-1.es.amazonaws.com/movies/bmovie'

def saveVideo (cat,vid,title,body):
  payload = {}
  payload['cat'] = cat
  payload['id'] = vid
  payload['title'] = title
  payload['body'] = body
  response = requests.post(url, data=json.dumps(payload))
  return response

def fetchVideo (cat,pt):
  payload = {}
  payload['c'] = cat
  payload['pt'] = pt
  response = requests.post(fetch_url, data=json.dumps(payload))
  return response

def postVideoToESS (video):
  # use the same ID of YT as ESS index document ID
  response = requests.post(ess_url+'/'+video['id'], data=json.dumps(video))
  return response
