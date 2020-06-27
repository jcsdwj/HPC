#生成文件
import sys,os

def createData():#创建一组数据
    path=sys.argv[0].replace("createData.py","")

    fo = open(path+"data1.txt", "w")
    for i in range(500000):#1-1000
        #data.append(i+1)
        fo.write(str(i+1))#以\t来作为分隔符
        if (i+1)%10==0 and (i+1)!=500000:
            fo.write("\n")#换行
        else:
            fo.write('\t')
    #fo.write("end")#结束符
    fo.close()
    #return data

createData()

#path=sys.argv[0].replace("createData.py","data.txt")
# f = open(path,'rb')
# for line in f:
#     print(line)
# print(path)
#filesize = str(os.path.getsize(path))#文件大小
# fname1, fname2 = os.path.split(path)
#print(filesize)
# print(fname1)#文件路径
# print(fname2)#文件名