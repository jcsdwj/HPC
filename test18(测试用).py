import socket,os
from multiprocessing import Process

def openFile():
    os.system("python /home/wj/桌面/final/compute1.py")  # 打开计算节点.py

openSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
openSocket.bind(('127.0.0.1',9003))
message=openSocket.recv()
print(message.decode())

# def startCompute():#打开三个计算节点
#     i=0
#     while i<3:
#         i=i+1
#         p=Process(target=openFile,args=())
#         p.start()
        

# def recv1():#第一次接收
#     j=0
#     while 1:#接收再发送
#         if j<3:
#             message,addr=openSocket.recvfrom(1025)
#             if(message.decode()!=''):
#                 j+=1
#                 print(message.decode())
#                 openSocket.sendto('我是大哥'.encode(),addr)
#         else:
#             break     
# def recv2():#第二次接收
#     k=0
#     while 1:
#         if k<3:
#             message=openSocket.recv(1025)
#             if(message.decode()!=''):
#                 k+=1
#                 print(message.decode())
#         else:
#             break

# startCompute()
# recv1()#最好设为异步的
# recv2()