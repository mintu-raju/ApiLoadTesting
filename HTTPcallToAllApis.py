from pytz import *
import re
import datetime
import pytz
import requests

BranchUuids = set()
BranchAccessTokens = {}
min_window = 19
max_window = 21
with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as logs:
    for line in logs:
        if (not '/v2/online_order/' in line) & (
                not '/index/tasks/updates/count/' in line) & (not '/online_item' in line):
            extractedList = line.split('"')
            TimeDurations = extractedList[0].split()
            match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', TimeDurations[5])
            capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
            datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
            datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
            hr = int(datetime_ist.strftime('%H'))  # taking hour to check peaks

            if hr <= max_window & hr >= min_window:
                apiDetails = extractedList[1].split()
                RequestType = extractedList[1].split(" ")[0]
                if RequestType == "GET":
                    apiUrl = extractedList[1].split(" ")[1]
                    ApiUrl = "https://v2staging.weavedin.com" + apiUrl
                    uuidPattern = re.compile(r'\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b')
                    u = re.search(uuidPattern, ApiUrl)
                    if (not u == None):
                        if uuidPattern.match(u.group()):  # CHECKING IF UUID IS PRESENT INORDER TO GET ACCESS TOKEN
                            if '/index/'in ApiUrl:
                                print("for index  "+u.group())
                                #code for adding seesion token to be inserted

                            if not (BranchAccessTokens.__contains__(u.group())):
                                accessResponse = requests.get(
                                    "https://v2staging.weavedin.com/api/branch/" + u.group() + "/device/register/" + "4EH80000OP8932" + "/" + "mobile" + "/",
                                    auth=(
                                    'admin@weavedin.com', 'weavedindemo76k'))  # to get access token against uuids
                                if accessResponse.status_code == 200:

                                    AccessToken = accessResponse.json()
                                    BranchAccessTokens[u.group()] = AccessToken[
                                        "token"]  # ADDING ACCESS TOKEN TO DICTIONARY

                            if BranchAccessTokens.__contains__(u.group()):
                                try:
                                    GetResponse = requests.get(ApiUrl, auth=('admin@weavedin.com', 'weavedindemo76k'),
                                                               headers={"Authorization": "Token " + BranchAccessTokens[
                                                                   u.group()]})
                                    print(GetResponse, GetResponse.elapsed.total_seconds())
                                except:
                                    print(ApiUrl + "  inside first except...")
                    else:  # WHEN NO UUID IS PRESENT SIMPLY POSTING THE REQUEST WITH URL
                        try:
                            GetResponse = requests.get(ApiUrl, auth=('admin@weavedin.com', 'weavedindemo76k'))
                            print(GetResponse, GetResponse.elapsed.total_seconds())
                        except:
                            print("   api failed, inside except...")
