import sys,socket,json

ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ServerSocket.bind(('127.0.0.1',9009))#这个是与客户端通信的，TCP的
ServerSocket.listen(5)
print("等待客户端连接")


def getDatafromClient():#新方法，从客户端接收消息
    ClntSocket, ClntAddr = ServerSocket.accept()
    Mixdata=ClntSocket.recv(1024).decode()#先发送的混合数据（包含节点数，文件名，文件大小)
    ClntSocket.sendto("1".encode(),ClntAddr)#表示已经收到消息了
    data=json.loads(Mixdata,strict=False)#数据是拼接的
    filename=str(data[0])#文件名
    filesize=int(data[1])#文件大小
    getFileSize=0
    #lineNum=0#文件行数
    
    f = open(sys.argv[0].replace('SendFileServer.py','newData.txt'),"wb")#以二进制格式写入_new文件
    while getFileSize<filesize:#　这里可能会有点问题
        fileData=ClntSocket.recv(1024)#会多接收数据
        getFileSize+=len(fileData)
        f.write(fileData)#写入文件
        #lineNum+=1#接收一条数据，文件行数+1
    ClntSocket.send("111".encode())
    print('接收行数中')

    lineNum=ClntSocket.recv(1024).decode()#接收文件行数

    f.close()
    print("接收到一个大小为",filesize,"的文件",filename)
    print("一共有",lineNum,"行")

getDatafromClient()
ServerSocket.close()