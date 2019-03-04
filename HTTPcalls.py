from pytz import *
import re
import datetime
import pytz
import requests
import random
import json

BranchAccessTokens = {}
min_window = 19
max_window = 21
with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as logs:
    for line in logs:
        if '/orders/ HTTP/1.1" 20' in line:

            extractedList = line.split('"')
            TimeDurations = extractedList[0].split()
            match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', TimeDurations[5])
            capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
            datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
            datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
            hr = int(datetime_ist.strftime('%H'))  # taking hour to check peaks
            if hr <= max_window & hr >= min_window:
                apiDetails = extractedList[1].split()
                apiUrl = apiDetails[1]
                ApiUrl = "https://v2staging.weavedin.com" + apiUrl
                RequestBody = str(extractedList[7])
                if RequestBody != "-":
                    uuidKey = line.split('"')[1].split()[1].split('/')[3]
                    if not (BranchAccessTokens.__contains__(uuidKey)):
                        accessResponse = requests.get(
                            "https://v2staging.weavedin.com/api/" + "branch/" + uuidKey + "/device/register/" + "4EH80000OP8932" + "/" + "mobile" + "/",
                            auth=('admin@weavedin.com', 'weavedindemo76k'))  # to get access token against uuidds
                        if accessResponse.status_code == 200:
                            AccessToken = accessResponse.json()
                            BranchAccessTokens[uuidKey] = AccessToken["token"]
                    if BranchAccessTokens.__contains__(uuidKey):
                        RequestBody = RequestBody.replace('\\x0A', '\n').replace('\\x22', '\"').replace('\\x5C', '\\')
                        try:
                            BodyJson = json.loads(RequestBody)
                            BodyJson["invoiceId"] = str(random.randint(100000, 99999999))#randomizing invoice id
                            for b in BodyJson["orders"]:
                                del b["online_transaction_id"]
                            #print(BodyJson)
                            OrderResponse = requests.post(ApiUrl, json=BodyJson,
                                                      auth=('admin@weavedin.com', 'weavedindemo76k'),
                                                      headers={"Authorization": "Token " + BranchAccessTokens[uuidKey]}) #hitting order api
                            print(OrderResponse.json(), OrderResponse.elapsed.total_seconds(),OrderResponse)
                        except:
                            #print(RequestBody)
                            print("inside except block.....")
