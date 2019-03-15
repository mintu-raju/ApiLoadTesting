import datetime, re
import pytz
from pytz import *
#API HIT IN A WINDOW SPAN
min_window=19
max_window=21

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1, open(
        "/home/mintu/essentials/Smart Retail/logs/Api Lists/GETapiCalledInaWindow", "w+") as file:
    # file.write("\nApi calls happened with peak order hour: \n\n")
    for s1l1 in serv1log1:
        extractedList = s1l1.split('"')
        TimeDurations = extractedList[0].split()
        match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', s1l1)
        capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
        datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
        datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
        hr = int(datetime_ist.strftime('%H'))
        apiDetails = extractedList[1].split()
        RequestType = apiDetails[0]
        apiUrl = apiDetails[1]
        Response = extractedList[2].split()
        ResponseCode = Response[0]
        #API HITS BETWEEN MIN_WINDOW & MAX_WINDOW OF TYPE GET AND STATUS200
        if (hr <= max_window & hr >= min_window) & (RequestType=="GET") & (ResponseCode=="200"):
            file.write(
                "Request Type: " + RequestType + "   API Url: " + apiUrl + "\n")
file.close()
