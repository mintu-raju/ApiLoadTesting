from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://username:password@ip_address:port/database')
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
    conn.execute('insert into user_permission_association values(%s, %s)',admin_id[0], permission_id[0])
