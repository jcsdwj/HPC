# -*- coding: utf-8 -*-
"""
Created on 2020/5/14 21:46

@author: wj
"""

#负责打开四个节点,管理计算节点
#这些节点我先让其都与server通信
#再让它用tcp与计算节点通信，收到标记
#我觉得可能要多进程处理这个问题了

import os,socket,json,math,time
from multiprocessing import Process

ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ServerSocket.bind(('127.0.0.1',9001))#这个是与客户端通信的，TCP的
ServerSocket.listen(5)

def getDatafromClient():#从客户端得到消息
    ClntSocket, ClntAddr = ServerSocket.accept()
    Mixdata=ClntSocket.recv(4096*200).decode()#这里接收的数据大小要设置大一些
    #Mixdata=json.loads(Mixdata)#转化为列表格式
    return Mixdata,ClntSocket,ClntAddr
    #包含节点数和数据集,客户端套接字和地址
    #print(Mixdata[0])

def detach(s,n,m):#拆分数据
#s为数据集，n为len(s),m为节点数，k为节点编号,拆分成m份
    #num=math.ceil(n/m)#向上取整来拆分
    num=math.floor(n/m)
    data= [s[i:i+num] for i in range(0, len(s), num)]
    #生成的拆分列表
    return data#多数据列表


#data=detach(data[1])#这些要发送给计算节点


def openFile():#这里应该是打开接收的.py文件，用它来计算
    os.system("python /home/wj/桌面/final/compute1.py")  # 打开计算节点.py


openSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#用来打开计算节点的套接字
openSocket.bind(('127.0.0.1',9003))

data,clntsocket,clntaddr=getDatafromClient()#从客户端接收数据
data=json.loads(data,strict=False)#数据是拼接的
newData=json.loads(data[1])
#print(len(newData))
#print('data类型为',type(data))
#data=json.loads(data)
#print('clntsocket为',clntsocket)
#print('clntaddr为',clntaddr)
num=int(data[0])#节点个数
#openSocket.listen(num)#监听节点个数
#udp不开启listens

#print('节点数为:',num)
#print('传过来的数据为',data)
#print(data[1])
#print(len(data[1]))
#print(num)
detachData=detach(newData,len(newData),num)#将数据拆分成num份
#data=detach(data[1],len(data),num)
#print(detachData)

def startCompute():#打开num个计算节点
    i=0
    num=data[0]#节点个数
    while i<int(num):
    #while i<3:     
        i=i+1
        p=Process(target=openFile,args=())
        p.start()
        time.sleep(1)


#data=[1,2,3,4,5,6,7,8,9,10]


Addr=[]#存放计算节点地址

def recv1():#第一次接收,收到消息表明已经和计算节点连上了
    j=0
    while 1:#接收再发送
        #如果突然有一个节点挂掉，怎么让程序自己退出
        if j<num:#保证收到num次的验证消息
        #if j<3:
            message,addr=openSocket.recvfrom(1024)
            Addr.append(addr)#存放节点的地址
            if(message.decode()!=''):               
                print(message.decode())#打印计算节点的认证消息
                #sondata=data[j]#第j份数据
                sondata=detachData[j]
               # print('我要发送的data为:',sondata)

               #这里发送数据太多，需要设置发送量
                openSocket.sendto(json.dumps(sondata).encode(),addr)#发送数据给计算节点
                j+=1
        else:
            break

Max=[]#三个最大值放入Max中
def recv2():#第二次接收，接收计算节点发来的最大值
    k=0
    while 1:
        if k<num:
            message=openSocket.recv(1025)#找了最大值
            # if(message.decode()!=''):
            #     k+=1
            #     print(message.decode())
            if message.decode()!='': 
                smallMax=message.decode()#收到的最大值
               # print('我收到的数据为',message.decode())
                print('收到的第%d最大值为:' %k,smallMax)
                Max.append(int(smallMax))#放入Max列表中        
                #if int(smallMax)>max:
                    #max=int(smallMax)
                    #print('第%d个max是' %k,max)
                k+=1    
                #return max
        else:
            break

#把算到的最大值发送给计算节点
def SendMax():#发送得到的最大值，我觉得可以用广播来做
    FinalMax=max(Max)
    #print('最大值为')
    for i in Addr:
        print('我发送最大值 %d' %FinalMax,'给',i)
        openSocket.sendto(str(FinalMax).encode(),i)#把最大值发送出去

maxCoprime=[]#最大互质值
def recv3():#得到最大互质数
    m=0
    while 1:
        if m<num:
            message=openSocket.recv(1024).decode()
            if message!='':
                print('我收到的第%d互质数为:' %m,message)
                maxCoprime.append(int(message))
                m+=1
        else:
            break


#计算节点发送第一次的计算数据给server

#这里面的时间还包括数据传输的时间
start=time.time()
startCompute()
recv1()
#time.sleep(1)
recv2()
#time.sleep(1)
SendMax()
#time.sleep(1)
recv3()

FinalMax=max(Max)#最大值
#print('最大值为',FinalMax)
maxPrime=max(maxCoprime)#这个要发送给客户端的
end=time.time()
print("计算总用时为:%.2f秒"%(end-start-4))#减４是因为打开４个计算节点里面停了４s


#print('最大互质数为',maxPrime)
result=[FinalMax,maxPrime]#拼接好
clntsocket.send(json.dumps(result).encode())#发送数据给客户端
print('数据发送完成')
