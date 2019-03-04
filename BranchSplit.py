import datetime, re
import pytz
from pytz import *

BranchCount = {}
min_window = 19
max_window = 21
with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1:
    for s1l1 in serv1log1:
        if '/orders/ HTTP/1.1" 20' in s1l1:
            uuidKey = s1l1.split('"')[1].split()[1].split('/')[3]
            BranchCount[uuidKey] = 0
with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1:
    for s1l1 in serv1log1:
        if '/orders/ HTTP/1.1" 20' in s1l1:
            extractedList = s1l1.split('"')
            TimeDurations = extractedList[0].split()
            match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', s1l1)
            capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
            datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
            datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
            hr = int(datetime_ist.strftime('%H'))
            if hr <= max_window & hr >= min_window:
                apiDetails = extractedList[1].split()
                RequestType = apiDetails[0]
                apiUrl = apiDetails[1]
                branchUuid = apiUrl.split('/')[3]
                BranchCount[branchUuid] += 1
print(BranchCount)
