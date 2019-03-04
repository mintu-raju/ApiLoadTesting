import datetime, re
import pytz
from pytz import *

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as f:
    for line in f:
        if 'v2/online_orders/' in line:

             #EXTRACTING RESPONSE TIME AND TIMESTAMP IN IST
             extractedList=line.split('"')
             TimeDurations=extractedList[0].split( )
             ResponseTime=TimeDurations[0]
             match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', TimeDurations[5])
             capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
             datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
             datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))

             #EXTRACTING REQUEST TYPE ,API URL,RESPONSE CODE & REQUEST BODY
             apiDetails=extractedList[1].split( )
             RequestType=apiDetails[0]
             apiUrl=apiDetails[1]
             Response=extractedList[2].split( )
             ResponseCode=Response[1]
             RequestBody= extractedList[7]

             #PRINTING ALL DETAILS
             print ("Response Time: "+ResponseTime +"\n")
             print("Timestamp in IST: " + datetime_ist.strftime("%Y-%m-%d %H:%M:%S %Z%z")+"\n")
             print("Request Type: " + RequestType+"\n")
             print("API Url: " + apiUrl+"\n")
             print("Response Code: " + ResponseCode+"\n")
             print("Request Body: " + RequestBody+"\n\n")






