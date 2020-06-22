# -*- coding: utf-8 -*-

import socket,json

def createData():#创建一组数据
    data=[]
    #fo = open("1.txt", "w")
    for i in range(100000):#1-1000
        data.append(i+1)
        #fo.write(str(data)+'\n')
    #fo.close()
    return data
#正常来说是读取数据

#自己解析文件中的数据，并保存
#def readData(filepath):
    


ClntSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ClntSocket.connect(('127.0.0.1',9001))#连接服务端
ClntSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096*200)#设置传输数据大小

def sendDatatoServer():

    data=createData()#这个数据发送给服务端

    num=input('请输入需要几个节点用来计算:')

    json_string = json.dumps(data)
#ClntSocket.send(num.encode())#把需要的节点发送过去
#ClntSocket.sendto(json_string.encode(),('127.0.0.1',9001))#把数据集发送给server
    Mix=[num,json_string]
    Mix_string = json.dumps(Mix)#混合，这样子就没有先来后到了

    ClntSocket.sendto(Mix_string.encode(),('127.0.0.1',9001))

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


sendDatatoServer()
getResult()
ClntSocket.close()