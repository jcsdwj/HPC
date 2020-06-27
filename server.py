# -*- coding: utf-8 -*-
"""
Created on 2020/5/14 21:46

@author: wj
"""

#负责打开四个节点,管理计算节点
#这些节点我先让其都与server通信
#再让它用tcp与计算节点通信，收到标记
#我觉得可能要多进程处理这个问题了

import os,socket,json,math,time,sys
from multiprocessing import Process



# def getDatafromClient():#从客户端得到消息
#     ClntSocket, ClntAddr = ServerSocket.accept()
#     Mixdata=ClntSocket.recv(4096*50).decode()#这里接收的数据大小要设置大一些
#     #Mixdata=json.loads(Mixdata)#转化为列表格式
#     return Mixdata,ClntSocket,ClntAddr
#     #包含节点数和数据集,客户端套接字和地址
#     #print(Mixdata[0])

def getDatafromClient():#新方法，从客户端接收消息
    ClntSocket, ClntAddr = ServerSocket.accept()
    Mixdata=ClntSocket.recv(1024).decode()#先发送的混合数据（包含节点数，文件名，文件大小)
    ClntSocket.sendto("1".encode(),ClntAddr)#表示已经收到消息了
    data=json.loads(Mixdata,strict=False)#数据是拼接的
    num=int(data[0])#节点编号
    filename=str(data[1])#文件名
    filesize=int(data[2])#文件大小
    getFileSize=0
    #lineNum=0#文件行数
    f = open(sys.argv[0].replace("server.py","new_"+filename),"wb")#以二进制格式写入_new文件,文件应该是new_data.txt
    while getFileSize<filesize:#　这里可能会有点问题
        fileData=ClntSocket.recv(1024)
        getFileSize+=len(fileData)
        f.write(fileData)#写入文件
        #lineNum+=1#接收一条数据，文件行数+1
    ClntSocket.send("1".encode())#代表接收完了
    f.close()
    print("接收到一个大小为",filesize,"的文件",filename)
    lineNum=ClntSocket.recv(1024).decode()#接收文件行数
    print('该文件的行数为',lineNum)
    return num,filename,lineNum,ClntSocket,ClntAddr#返回节点数和文件名

    #return Mixdata,ClntSocket,ClntAddr

#用udp发送文件给计算节点，让他们自己去拆分
#用不到了
def detach(s,n,m):#拆分数据
#s为数据集，n为len(s),m为节点数，k为节点编号,拆分成m份
    #num=math.ceil(n/m)#向上取整来拆分
    num=math.floor(n/m)
    data= [s[i:i+num] for i in range(0, len(s), num)]
    #生成的拆分列表
    return data#多数据列表

def detachFile(num,filename,lineNum):#拆分成num个文件
    #拆分的份数，文件名,文件行数
    #按行数拆分，条件是数据得均匀
    flag=0#计算行数
   # dataList=[]
    F=open(filename,"r")
    smallFileLine=math.floor(lineNum/num)#一份文件的长度,向上取整
    #总行数除以份数
    #print(smallFileLine)

    DirPath=[]
    for i in range(num):
        dirpath=sys.argv[0].replace("server.py","split/splitData"+str(i)+".txt")#切分后的文件名
        DirPath.append(dirpath)#文件名列表

    ｉ=0
    for Line in F.readlines():#读一行
        if flag==0:#根据flag来打开文件
            f=open(DirPath[i],"w")#打开子文件
        if flag<smallFileLine:       
            if i<num-1:
                flag+=1
                f.writelines(Line)
                if flag==smallFileLine:#如果到了数据量
                    #flag=0#重新赋值为0
                    flag=0
                    i+=1#重新打开文件
            else:
                f.writelines(Line)
                flag+=1
#data=detach(data[1])#这些要发送给计算节点


def openFile():#这里应该是打开接收的.py文件，用它来计算
    os.system("python /home/wj/桌面/final/compute1.py")  # 打开计算节点.py

def startCompute(num):#打开num个计算节点
    i=0
    #num=data[0]#节点个数
    while i<int(num):
    #while i<3:     
        i=i+1
        p=Process(target=openFile,args=())
        p.start()
        time.sleep(2)

#def SendFileToCompute(addr):#发送数据给计算节点


def recv1():#第一次接收,收到消息表明已经和计算节点连上了
    #发送序列号给计算节点让他们更新文件名
    Addr=[]
    j=0
    while 1:#接收再发送
        #如果突然有一个节点挂掉，怎么让程序自己退出
        if j<num:#保证收到num次的验证消息
        #if j<3:
            message,addr=openSocket.recvfrom(1024)
            Addr.append(addr)#存放计算节点的地址
            if(message.decode()=='你是大哥'):  #这是验证消息             
                print("收到节点",j,"的验证消息")#打印计算节点的认证消息
                #sondata=data[j]#第j份数据

                #这里发送文件给计算节点
                f=open(sys.argv[0].replace("server.py","split/splitData")+str(j)+".txt","rb")#打开这个文件
                filesize = os.path.getsize(sys.argv[0].replace("server.py","split/splitData")+str(j)+".txt")#读取文件大小
                r1message=[j,filesize]
                
                r1message_json=json.dumps(r1message)#第一个是编号，第二个是文件大小
                openSocket.sendto(r1message_json.encode(),addr)#发送文件大小给连上的节点　　
                #print('我把文件大小和编号发给计算节点了')
                print('发送的文件为',sys.argv[0].replace("server.py","split/splitData")+str(j)+".txt")
                print('文件大小为',filesize)
                print('节点编号为',j)
                #计算节点把下面的消息也接收了
                #news=openSocket.recv(1024).decode()#收到验证消息才给发消息
                #print("我收到的验证消息是",news)
                #if news=="I get":#收到验证消息再进行下一步
                time.sleep(1)#停１s
                while 1:
                    for line in f.readlines():#分块发送计算文件
                        openSocket.sendto(line,addr)#一般udp用sendto，但tcp也能用
                        #后面几个数为啥接收不到
                    break
                j+=1
                
    
            #     sondata=detachData[j]
            #    # print('我要发送的data为:',sondata)

            #    #这里发送数据太多，需要设置发送量
            #     openSocket.sendto(json.dumps(sondata).encode(),addr)#发送数据给计算节点
            #     j+=1
        else:
            break
    return Addr#计算节点地址

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
                print('收到的第%d个最大值为:' %k,smallMax)
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

ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ServerSocket.bind(('127.0.0.1',9001))#这个是与客户端通信的，TCP的
ServerSocket.listen(5)
print("等待客户端连接")

openSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#用来打开计算节点的套接字
openSocket.bind(('127.0.0.1',9003))

num,filename,lineNum,clntsocket,_=getDatafromClient()#从客户端得到数据

#detachData=detach(newData,len(newData),num)#将数据拆分成num份
detachFile(num,filename,int(lineNum))#将文件拆分成num个

Addr=[]#存放计算节点地址
Max=[]#三个最大值放入Max中

maxCoprime=[]#最大互质值
#计算节点发送第一次的计算数据给server

#这里面的时间还包括数据传输的时间
start=time.time()
startCompute(num)#打开计算进程，正常是计算节点
Addr=recv1()
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
print("计算总用时为:%.2f秒"%(end-start-2*num-num))#有num个节点,每个进程开启需要２s,recv1里面停了1s
#print('最大互质数为',maxPrime)
result=[FinalMax,maxPrime]#拼接好
clntsocket.send(json.dumps(result).encode())#发送数据给客户端
print('数据发送完成')
ServerSocket.close()
openSocket.close()

#data,clntsocket,clntaddr=getDatafromClient()#从客户端接收数据
#data=json.loads(data,strict=False)#数据是拼接的
#newData=json.loads(data[1])
#num=int(data[0])#节点个数

#print(len(newData))
#print('data类型为',type(data))
#data=json.loads(data)
#print('clntsocket为',clntsocket)
#print('clntaddr为',clntaddr)

#openSocket.listen(num)#监听节点个数
#udp不开启listens

#print('节点数为:',num)
#print('传过来的数据为',data)
#print(data[1])
#print(len(data[1]))
#print(num)

#data=detach(data[1],len(data),num)
#print(detachData)

#data=[1,2,3,4,5,6,7,8,9,10]

#openSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096*100)

