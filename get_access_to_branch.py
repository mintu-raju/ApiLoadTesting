from pytz import *
import re
import datetime
import pytz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests

BranchUuids = set()
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
                    # if len(apiUrl.split("/")) > 4:
                    uuidPattern = re.compile(r'\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b')
                    u = re.search(uuidPattern, ApiUrl)
                    if (not u == None):
                        if uuidPattern.match(u.group()):  # CHECKING IF UUID IS PRESENT INORDER TO GET ACCESS TOKEN
                            # print(uuidKey)
                            if '/index/' in ApiUrl:
                                BranchUuids.add(u.group())

BranchUuidsList=list(BranchUuids)
print(BranchUuidsList)
engine = create_engine(
    'mysql+pymysql://v2-staging-user:TridEud3@store-staging-06-02-2019.ctkejhwhh9do.ap-southeast-1.rds.amazonaws.com/v2prod')

conn = engine.connect()
session = sessionmaker(bind=engine)

admin_id = conn.execute('select id from user where user_name=%s', 'Weavedin Admin').fetchone()

for index, branch_uuid in enumerate(BranchUuidsList):
    BranchUuidsList[index] = branch_uuid.replace('-', '')
for branch_uuid in BranchUuidsList:
    branch_id = conn.execute('select id from branch where hex(uuid)=%s', branch_uuid).fetchone()
    permission_id = conn.execute('select id from permission where organization= %s', branch_id[0]).fetchone()
    print(permission_id)
    db_row = conn.execute('select * from user_permission_association  where user=%s and permission=%s', admin_id[0],
                          permission_id[0]).fetchone()
    if db_row:
        branch_name=conn.execute('select name from branch where id=%s',branch_id[0]).fetchone()
        print(branch_name)
    #if not db_row:
       # conn.execute('insert into user_permission_association values(%s, %s)', admin_id[0], permission_id[0])
