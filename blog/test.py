# FileName : pgconn.py
# Author   : Adil
# DateTime : 2018/6/15 15:19
# SoftWare : PyCharm
import paramiko
import psycopg2
import pymysql
from sshtunnel import SSHTunnelForwarder

# 获取密钥
# private_key = paramiko.RSAKey.from_private_key_file('/Users/yyj/.ssh/id_rsa')
# with SSHTunnelForwarder(
#         # 指定ssh登录的跳转机的address
#         ssh_address_or_host=('121.41.94.18', 22),
#         # 设置密钥
#         # ssh_pkey = private_key,
#         # 如果是通过密码访问，可以把下面注释打开，将密钥注释即可。
#         ssh_password="7379002300Liu",
#         # 设置用户
#         ssh_username='root',
#         # 设置数据库服务地址及端口
#         remote_bind_address=('127.0.0.1', 3306),
#         # 开启本地转发端口
#         local_bind_address=('127.0.0.1', 9999),
# ) as server:
server = SSHTunnelForwarder(ssh_address_or_host=('121.41.94.18', 22),  # 跳板机B地址
                            # ssh_port=22,  # 跳板机B端口
                            ssh_username='root',
                            ssh_password='7379002300Liu',
                            local_bind_address=('127.0.0.1', 99),  # 这里必须填127.0.0.1
                            remote_bind_address=('127.0.0.1', 3306)  # 目标机器A地址，端口
                            )
server.start()
# server.start()
print(server.local_bind_port)
# conn = psycopg2.connect(database='blog',
#                         user='blog',
#                         password='3mGND6yELS5JE6KZ',
#                         host='127.0.0.1',  # 因为上面没有设置 local_bind_address,所以这里必须是127.0.0.1,如果设置了，取设置的值就行了。
#                         port = server.local_bind_port  # 这里端口也一样，上面的server可以设置，没设置取这个就行了
#                         )
# print(conn)
#
# cur = conn.cursor()
# # 执行查询，查看结果，验证数据库是否链接成功。
# cur.execute("select * from t_table_data limit 1")
#
# rows = cur.fetchone()
#
# print(rows)
#
# conn.close()
conn = pymysql.connect(
    host='127.0.0.1',
    port=server.local_bind_port,
    user='blog',
    password='3mGND6yELS5JE6KZ',
    db='blog',
    charset='utf8'
)
cursor = conn.cursor()
print(cursor)
# cursor.execute(sql, params)
# rows = cursor.fetchall()
# # conn.commit()
# cursor.close()
# conn.close()
