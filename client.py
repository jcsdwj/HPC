# -*- coding: utf-8 -*-

import socket,json,sys,os,time

def createData():#创建一组数据
    data=[]
    #fo = open("1.txt", "w")
    for i in range(10000):#1-1000
        data.append(i+1)
        #fo.write(str(data)+'\n')
    #fo.close()
    return data
    #这个用不到了
#正常来说是读取数据

def SendFiletoServer():#发送文件给server,先发送节点数和文件名，再发送文件
    num=input('请输入需要几个节点用来计算:')
    filepath=sys.argv[0].replace("client.py","data1.txt")#待发送文件的路径
    fread = open(filepath,'rb')#二进制读文件
    filesize = str(os.path.getsize(filepath))#文件大小
    _, fname2 = os.path.split(filepath)#路径和文件名
    dataBag=[str(num),fname2,str(filesize)]#节点数，文件名,文件大小
    dataBag_json=json.dumps(dataBag)
    ClntSocket.sendto(dataBag_json.encode(),('127.0.0.1',9001))#先将混合数据发送过去

    time.sleep(1)#保证能收到消息
    
    flag='0'
    flag=ClntSocket.recv(1024).decode()
    lineNum=0
    while 1:#接收到消息再发送
        if flag!='0':
            for line in fread.readlines():#发送文件
                ClntSocket.sendto(line,('127.0.0.1',9001))#一般udp用sendto，但tcp也能用
                lineNum+=1
            break
    while 1:#接收一个验证消息再发送行数给服务端
        message=ClntSocket.recv(1024).decode()
        if message:
            ClntSocket.send(str(lineNum).encode())
            break
    

# def sendDatatoServer():#这里应该要做到发送计算任务文件和计算文件

#     data=createData()#这个数据发送给服务端

#     num=input('请输入需要几个节点用来计算:')

#     json_string = json.dumps(data)
# #ClntSocket.send(num.encode())#把需要的节点发送过去
# #ClntSocket.sendto(json_string.encode(),('127.0.0.1',9001))#把数据集发送给server
#     Mix=[num,json_string]
#     Mix_string = json.dumps(Mix)#混合，这样子就没有先来后到了

#     ClntSocket.sendto(Mix_string.encode(),('127.0.0.1',9001))

#sendDatatoServer()

def getResult():
    while 1:
        result=ClntSocket.recv(1024).decode()     
        if result!='':
            res = json.loads(result)
            #Max=int(res[0])
            #MaxPri=int(res[1])
            print('最大数为',res[0])
            print('最大互质数为',res[1])
            break

ClntSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ClntSocket.connect(('127.0.0.1',9001))#连接服务端
#ClntSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096*50)#设置传输数据大小
#tcp是数据流协议，因此不存在包大小的限
#udp用sendto函数有最大发送数据长度，如果大于这个长度会报错
SendFiletoServer()
#sendDatatoServer()
getResult()
ClntSocket.close()