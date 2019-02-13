# -*- coding: utf-8 -*-

import os
from service import *

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def videos_list_multiple_ids(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()

  return print_response(response)


if __name__ == '__main__':
  client = get_service()
  
  videos_list_multiple_ids(client,
    fields='items(id, snippet/defaultAudioLanguage, snippet/defaultLanguage, snippet/publishedAt, snippet/title, snippet/channelId, snippet/channelTitle, contentDetails/duration)',
    part='snippet,contentDetails,statistics',
    id='Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI')
  
