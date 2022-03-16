import json
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import requests
import sys
import unidecode
from datetime import datetime

inputDay = '2022-03-15'

def send_to_slack(message):
        url = 'https://hooks.slack.com/services/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'
        headers = {'Content-type': 'application/json'}
        data = '{{"text":"{0}"}}'.format(message)
        response = requests.post(url, headers=headers, data=data.encode('utf-8'))
        print(response.text)
        print(response.status_code)



message = "top_login for {0}: {1}".format(inputDay, 'luq89')

unicodeMessage = unidecode.unidecode(message)

send_to_slack(message)
