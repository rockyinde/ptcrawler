import requests
import json

url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/save'
ess_url = 'https://search-tmovies-h6qlkaunfxq6rrnd7fqoot7cuu.ap-south-1.es.amazonaws.com/movies/movie'
save_url_v2 = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/savev2'

# builds the payload to post to DDB/ESS
def buildPayload (cat, vid, title, body):
  
  payload = {}
  payload['cat'] = cat
  payload['id'] = vid
  payload['title'] = title
  payload['body'] = body

  return payload

# saves the video to DDB
def saveVideo (cat,vid,title,body):

  payload = buildPayload(cat, vid, title, body)
  response = requests.post(url, data=json.dumps(payload))
  return response

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

# posts the video to ESS for indexing
def saveVideoToESS (cat,vid,title,body):

  payload = buildPayload(cat, vid, title, body)

  # use the same ID of YT as ESS index document ID
  headers = {'content-type': 'application/json'}
  response = requests.post(ess_url+'/'+vid, data=json.dumps(payload),
                            headers = headers)
  return response
