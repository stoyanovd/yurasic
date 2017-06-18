import os

from googleapiclient.discovery import build
import pprint

my_api_key = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_TOKEN')
my_cse_id = os.environ.get('GOOGLE_CSE_ID')


def inner_google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def google_search(s):
    results = inner_google_search(s, my_api_key, my_cse_id, num=10)

    ans = str()
    for result in results:
        pprint.pprint(result, stream=ans)
    return ans
