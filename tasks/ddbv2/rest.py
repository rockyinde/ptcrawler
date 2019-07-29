import requests
import json

url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/save'
save_url_v2 = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/savev2'
fetch_url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/videos'
ess_url = 'https://search-tmovies-h6qlkaunfxq6rrnd7fqoot7cuu.ap-south-1.es.amazonaws.com/movies/movie'

# schema for V2
def saveVideoV2 (vid,cat,title,likes,views,perc,pdate,tags,body):
  payload = {}
  payload['id'] = vid
  payload['cat'] = cat
  payload['title'] = title
  payload['likes'] = likes
  payload['views'] = views
  payload['perc'] = perc
  payload['pdate'] = pdate
  payload['tags'] = tags
  payload['body'] = body
  response = requests.post(save_url_v2, data=json.dumps(payload))
  return response

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
  if pt is not None:
    payload['pt'] = pt
  response = requests.post(fetch_url, data=json.dumps(payload))
  return json.loads(response.content)

def postVideoToESS (video):
  # use the same ID of YT as ESS index document ID
  headers = {'content-type': 'application/json'}
  response = requests.post(ess_url+'/'+video['id'], data=json.dumps(video),
                            headers = headers)
  return response
