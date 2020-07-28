import requests
import json

ess_url = 'https://search-tmovies-h6qlkaunfxq6rrnd7fqoot7cuu.ap-south-1.es.amazonaws.com/hmovies/movie'
save_url = 'https://05wpjm20r7.execute-api.ap-south-1.amazonaws.com/prod/savev2'

# builds the payload to post to DDB/ESS
def buildPayload (udate, vid, title, body):
  
  payload = {}
  payload['udate'] = udate
  payload['id'] = vid
  payload['title'] = title
  payload['body'] = body
  payload['cat'] = 'n'

  return payload

# schema for V2
def saveVideoV2 (vid,udate,title,likes,views,perc,pdate,tags,body):
  payload = {}
  payload['id'] = vid
  payload['udate'] = udate
  payload['title'] = title
  payload['likes'] = likes
  payload['views'] = views
  payload['perc'] = perc
  payload['pdate'] = pdate
  payload['tags'] = tags
  payload['body'] = body
  payload['cat'] = 'n'
  response = requests.post(save_url, data=json.dumps(payload))
  return response

# posts the video to ESS for indexing
def saveVideoToESS (udate,vid,title,body):

  payload = buildPayload(udate, vid, title, body)

  # use the same ID of YT as ESS index document ID
  headers = {'content-type': 'application/json'}
  response = requests.post(ess_url+'/'+vid, data=json.dumps(payload),
                            headers = headers)
  return response
