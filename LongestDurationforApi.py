import datetime, re
import pytz
from pytz import *

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1:
    startHour = "11"
    ResponseTimeList = []


    for s1l1 in serv1log1:
        extractedList = s1l1.split('"')
        TimeDurations = extractedList[0].split()
        match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', s1l1)
        capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
        datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
        datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
        hr = datetime_ist.strftime('%H')
        if '/v2/online_order/' in s1l1:
            ResponseTimeList.append(float(TimeDurations[0]))

ResponseTimeList.sort(reverse=True)

print("\nResponse Time : " + "\t")
print(*ResponseTimeList, sep=", ")
