import os
import urllib.parse

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

    ans = ["Search results: "]
    ans += ["len: " + str(len(results))]

    sites = []
    for result in results:
        sites += [urllib.parse.quote_plus(pprint.pformat(result))]

    ans = os.linesep.join(ans)
    ans = "ans len: " + str(len(ans)) + ans

    if len(ans) > 500:
        ans = ans[:500]
    return ans