import sys
import json
import datetime
import requests

import report

def gSearch(keyword, api_key, api_host):

    url = "https://google-search3.p.rapidapi.com/api/v1/search/q=" + keyword.replace(" ", "+") + "&num=10"
    print(url)

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': api_host
    }

    res = requests.request("GET", url, headers=headers)

    if(200 == res.status_code):
        return report.reports(json.loads(res.text))

    else:
        return None
