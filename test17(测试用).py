# -*- coding: utf-8 -*-
"""
Created on 2020/4/4 18:01

@author: wj
"""

import socket

data=""
for i in range(10000):
    data+=str(i)

stocSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#stocSocket.connect(('127.0.0.1',9003))#与server连接
stocSocket.sendto(data.encode(),('127.0.0.1',9003))#发送给server

# while 1:#接收
#     data = stocSocket.recv(1024).decode()  # 接收传过来的数组数据，不过还是要先转化
#     if data!='':
#         stocSocket.sendto('你依然是大哥'.encode(),('127.0.0.1',9003))
#         break