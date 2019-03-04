import re
import datetime
import pytz
from pytz import *

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as f:
    for line in f:
        match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', line)
        capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
        datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
        datetime_ist= datetime_gmt.astimezone(timezone('Asia/Kolkata'))
        print (datetime_ist.strftime(fmt))


