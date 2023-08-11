from sshtunnel import SSHTunnelForwarder

# server = SSHTunnelForwarder(ssh_address_or_host=('121.41.94.18', 22),  # 跳板机B地址
#                             # ssh_port=22,  # 跳板机B端口
#                             ssh_username='root',
#                             ssh_password='7379002300Liu',
#                             local_bind_address=('127.0.0.1', 99),  # 这里必须填127.0.0.1
#                             remote_bind_address=('127.0.0.1', 3306)  # 目标机器A地址，端口
#                             )
# server.start()
# print(server.local_bind_port)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': '127.0.0.1',
#         'PORT': server.local_bind_port,
#         'NAME': 'db_test',
#         'USER': 'jusr8pr5kbrj',
#         'PASSWORD': 'TbH9&UJR8LZh7oZ7'
#                     ''
#                     ''
#                     '',
#         'OPTIONS': {'sql_mode': 'traditional', }}}
