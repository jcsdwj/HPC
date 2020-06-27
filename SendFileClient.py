import sys,socket,json,os,time


ClntSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ClntSocket.connect(('127.0.0.1',9009))#连接服务端

def SendFiletoServer():#发送文件给server,先发送节点数和文件名，再发送文件
    #num=input('请输入需要几个节点用来计算:')
    filepath=sys.argv[0].replace("SendFileClient.py","data.txt")#待发送文件的路径
    fread = open(filepath,'rb')#二进制读文件
    filesize = str(os.path.getsize(filepath))#文件大小
    _, fname2 = os.path.split(filepath)#路径和文件名
    dataBag=[fname2,str(filesize)]#文件名,文件大小
    dataBag_json=json.dumps(dataBag)
    ClntSocket.sendto(dataBag_json.encode(),('127.0.0.1',9009))#先将混合数据发送过去
    time.sleep(1)#保证能收到消息
    flag='0'
    flag=ClntSocket.recv(1024).decode()
    lineNum=0
    while 1:#接收到消息再发送
        if flag!='0':
            for line in fread.readlines():#发送文件
                ClntSocket.sendto(line,('127.0.0.1',9009))#一般udp用sendto，但tcp也能用
                lineNum+=1
            break
    while 1:#接收一个验证消息再发送行数给服务端
        message=ClntSocket.recv(1024).decode()
        if message:
            ClntSocket.send(str(lineNum).encode())
            break

SendFiletoServer()
print("数据发送完了")