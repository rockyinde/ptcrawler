import requests
import json

url = 'https://a7fdcsp3ak.execute-api.ap-south-1.amazonaws.com/prod/save'

def saveVideo (cat,vid,title,body):
  payload = {}
  payload['cat'] = cat
  payload['id'] = vid
  payload['title'] = title
  payload['body'] = body
  response = requests.post(url, data=json.dumps(payload))
  return response
