import datetime, re
import pytz
from pytz import *

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as f, open(
        "/home/mintu/essentials/Smart Retail/logs/Api Lists/api_over1s_web1log2", 'w+') as w:
    for line in f:

            # EXTRACTING RESPONSE TIME AND TIMESTAMP IN IST
            extractedList = line.split('"')
            TimeDurations = extractedList[0].split()
            ResponseTime = TimeDurations[0]
            if float(ResponseTime) > 1:
                match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', TimeDurations[5])
                capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
                datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
                datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))

                # EXTRACTING REQUEST TYPE ,API URL,RESPONSE CODE & REQUEST BODY
                apiDetails = extractedList[1].split()
                RequestType = apiDetails[0]
                apiUrl = apiDetails[1]
                Response = extractedList[2].split()
                ResponseCode = Response[0]
                RequestBody = extractedList[7]

                # WRITING ALL DETAILS
                w.write("\nResponse Time: " + ResponseTime + "   Timestamp in IST: " + datetime_ist.strftime(
                "%Y-%m-%d %H:%M:%S %Z%z") + "   Request Type: " + RequestType + "   API Url: " + apiUrl + "   Response Code: " + ResponseCode + "   Request Body: " + RequestBody+"\n\n")
