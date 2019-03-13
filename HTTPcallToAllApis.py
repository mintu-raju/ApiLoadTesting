from pytz import *
import re
import datetime
import pytz
import requests
from bs4 import BeautifulSoup

BranchUuids = set()
BranchAccessTokens = {}
min_window = 19
max_window = 21
params = {}


def setCookie(session):
    url = "https://v2staging.weavedin.com/index/"
    soup = BeautifulSoup(session.get(url).text, "html.parser")
    csrfToken = soup.find(attrs={"id": "csrf_token"})
    params = {'email': 'admin@weavedin.com', 'password': 'weavedindemo76k', 'csrf_token': csrfToken['value'],
              'signIn': "Sign in"}
    response = session.post(url, data=params, headers=dict(referer=url))
    return (response.headers['Set-Cookie'])

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
            Response = extractedList[2].split()
            ResponseCode = Response[0]

            if hr <= max_window & hr >= min_window:
                apiDetails = extractedList[1].split()
                RequestType = extractedList[1].split(" ")[0]

                if RequestType == "GET" and ResponseCode == "200":
                    apiUrl = extractedList[1].split(" ")[1]
                    ApiUrl = "https://v2staging.weavedin.com" + apiUrl
                    uuidPattern = re.compile(r'\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b')
                    u = re.search(uuidPattern, ApiUrl)
                    if (not u == None) and not '/store/' in ApiUrl:
                        if uuidPattern.match(u.group()):  # CHECKING IF UUID IS PRESENT INORDER TO GET ACCESS TOKEN
                            if not (BranchAccessTokens.__contains__(u.group())) and not ('/index/' in ApiUrl):
                                accessResponse = requests.get(
                                    "https://v2staging.weavedin.com/api/branch/" + u.group() + "/device/register/" + "4EH80000OP8932" + "/" + "mobile" + "/",
                                    auth=(
                                        'admin@weavedin.com', 'weavedindemo76k'))  # to get access token against uuids
                                if accessResponse.status_code == 200:
                                    AccessToken = accessResponse.json()
                                    BranchAccessTokens[u.group()] = AccessToken[
                                        "token"]  # ADDING ACCESS TOKEN TO DICTIONARY

                            if BranchAccessTokens.__contains__(u.group()) and not ('/index/' in ApiUrl):
                                try:
                                    print(ApiUrl)
                                    GetResponse = requests.get(ApiUrl, auth=('admin@weavedin.com', 'weavedindemo76k'),
                                                               headers={"Authorization": "Token " + BranchAccessTokens[
                                                                   u.group()]})
                                    print(GetResponse, GetResponse.elapsed.total_seconds())
                                except:
                                    print(ApiUrl + "  inside first except...")
                    if '/index/' in ApiUrl:
                        session = requests.session()
                        print(ApiUrl)
                        cookie = setCookie(session)
                        GetResponse = session.get(ApiUrl, data=params,
                                                  headers={"Set-Cookie": cookie})
                        print(GetResponse, GetResponse.elapsed.total_seconds())

                    if ((u == None) and not '/index/' in ApiUrl) or ((
                                                                     not u == None) and '/store/' in ApiUrl):  # WHEN NO UUID IS PRESENT SIMPLY POSTING THE REQUEST WITH URL
                        try:
                            print(ApiUrl)
                            GetResponse = requests.get(ApiUrl, auth=('admin@weavedin.com', 'weavedindemo76k'))
                            print(GetResponse, GetResponse.elapsed.total_seconds())
                        except:
                            print("   api failed, inside except...")
