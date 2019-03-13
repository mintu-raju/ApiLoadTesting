from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://v2-staging-user:TridEud3@store-staging-06-02-2019.ctkejhwhh9do.ap-southeast-1.rds.amazonaws.com/v2prod')
# engine = create_engine('mysql://root:root@localhost/weaver_v2')
conn = engine.connect()
session = sessionmaker(bind=engine)

admin_id = conn.execute('select id from user where user_name=%s', 'Weavedin Admin').fetchone()

branch_uuid_list = ['9d7bee54-047a-4d99-84bc-9b85a03c656a']
for index, branch_uuid in enumerate(branch_uuid_list):
    branch_uuid_list[index] = branch_uuid.replace('-', '')
for branch_uuid in branch_uuid_list:
    branch_id = conn.execute('select id from branch where hex(uuid)=%s', branch_uuid).fetchone()
    permission_id=conn.execute('select id from permission where organization= %s',branch_id[0]).fetchone()
    db_row=conn.execute('select * from user_permission_association  where user=%s and permission=%s',admin_id[0],permission_id[0]).fetchone()
    if db_row:
        branch_name=conn.execute('select name from branch where id=%s',branch_id[0]).fetchone()
        print(branch_name)
    #if not db_row:
    	#conn.execute('insert into user_permission_association values(%s, %s)',admin_id[0], permission_id[0])
