# -*- coding: utf-8 -*-
"""
Created on 2020/5/14 21:43

@author: wj
"""

#计算节点

#我的想法就是让计算节点直接与server联系
import socket,json,sys

def ReadtoList(num):#读取文件返回成列表
    f=open(sys.argv[0].replace('compute1.py',"test/test"+str(num)+".txt"),'r')#读取文件，因为把接收的文件保存为test.txt文件了
    data=f.readlines()#按行存放的列表
    #需要解析
    Data=[]
    for i in data:
    #i.strip('\n')#先去除'\n'
        slist=i.strip('\n').split('\t')#按\t划分

        for j in slist:
            if j!='':
                Data.append(int(j))

    return Data#列表，里面数据为整型

def deal_data1(data):#处理接收的数据,找到最大值，这里可以直接用max()来做
    max=data[0]
    for i in data:
        if max<i:
            max=i
    return max#返回最大值

def is_Coprime(x,y):#判断两个数是否互质
    if x>1 and y>1:
        t=0
        if x<y:
            t=x
            x=y
            y=t
        while x%y:
            t=y
            y=x%y
            x=t
    if y==1:
        return True
    else:
        return False


def deal_data2(data,x):#找到最大与x互质的值
    Max=1
    for i in data:
        if is_Coprime(x,i) and i>Max:
            Max=i
    return Max

stocSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#stocSocket.connect(('127.0.0.1',9003))#与server连接
stocSocket.sendto('你是大哥'.encode(),('127.0.0.1',9003))#发送给open

Data=[]#用来存储发送过来的数据

while 1:#接收要计算的数据
    
    #data = stocSocket.recv(1024).decode()  # 接收传过来的数组数据，不过还是要先转化,这里接收的值要大些,recv里面必须要有参数
    #其实可以直接把接收的数据放入内存，我这先用文件保存
    message = stocSocket.recv(1024).decode()#先接收文件大小
    data = json.loads(message)
    num = data[0]
    filesize=data[1]
    f=open(sys.argv[0].replace("compute1.py","test/test"+str(num)+".txt"),"wb")#打开文件流接收文件,保存到test.txt,根据编号保存
    
    if filesize:#若接收到
        #stocSocket.sendto("I get".encode(),('127.0.0.1',9003)) 
        getFileSize=0
        while getFileSize<filesize:#当小于接收到的文件
            fileData=stocSocket.recv(1024)
            getFileSize+=len(fileData)
            f.write(fileData)
        f.close()
        Data=ReadtoList(num)
        Max=str(deal_data1(Data))#转化为str格式
        
        stocSocket.sendto(Max.encode(),('127.0.0.1',9003))#把算得的最大值发送过去
        break

    
    # #先把他们存入文件
    # if data!='':
    #     data=json.loads(data)#数据格式转化
    #     Data=data#保存数据
    #     Max=str(deal_data1(Data))#转化为str格式
    #     #stocSocket.sendto('你依然是大哥'.encode(),('127.0.0.1',9003))
    #     stocSocket.sendto(Max.encode(),('127.0.0.1',9003))
    #     break

        # data = json.loads(data)
        # Max = deal_data1(data)  # 找到最大值
        # stocSocket.sendto(str(Max).encode(),('127.0.0.1',9003))
        # Data=data#保存数据
        # break

while 1:
    max=stocSocket.recv(1024).decode()#收到的最大值
    if max!='':#得到最大值
        maxCoprime=deal_data2(Data,int(max)) 
        stocSocket.sendto(str(maxCoprime).encode(),('127.0.0.1',9003))
        break
    


#局域网广播
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# PORT = 1060
# s.bind(('', PORT))
# print('Listening for broadcast at ', s.getsockname())
# while True:
#     if data!='':
#         data, address = s.recvfrom(1024)
#         break
    #print('Server received from {}:{}'.format(address, data.decode('utf-8')))


# MMMaaaxxx=0
# while 1:
#     data = stocSocket.recv(1024).decode()  # 接收传过来的数组数据，不过还是要先转化
#     if data!='':
#         MMMaaaxxx=int(data)#得到最大值
#         break
#
# number=deal_data2(Data,MMMaaaxxx)