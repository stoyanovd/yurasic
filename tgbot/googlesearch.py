import os
import urllib.parse

import sys
from googleapiclient.discovery import build
import pprint

from langdetect import detect_langs

my_api_key = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_TOKEN')
my_cse_id = os.environ.get('GOOGLE_CSE_ID')


def inner_google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


CHORDS_EN = "chords"
CHORDS_RU = "аккорды"


def get_word_chords_in_lang(s):
    langs = detect_langs(s)
    if not langs:
        raise Exception("Can't guess lang (langdetect)")
    if langs[0] == 'en':
        return CHORDS_EN + " "
    if langs[0] == 'ru':
        return CHORDS_RU + " "
    print("Lang guess return " + str(langs) + " (but we want 'ru' or 'en' as first)", file=sys.stderr)
    return CHORDS_RU + " "


def google_search(s):
    results = inner_google_search(get_word_chords_in_lang(s) + s,
                                  my_api_key, my_cse_id, num=10)

    ans = ["Search results: "]
    ans += ["len: " + str(len(results))]

    sites = []
    for result in results:
        # sites += [urllib.parse.quote_plus(pprint.pformat(result))]
        sites += [pprint.pformat(result)]

    ans += sites

    ans = os.linesep.join(ans)
    ans = "ans len: " + str(len(ans)) + ans

    if len(ans) > 500:
        ans = ans[:500]
    return ans
